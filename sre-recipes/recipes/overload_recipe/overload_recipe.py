#
# Copyright 2021 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# -*- coding: utf-8 -*-
"""
This module contains the implementation of overload recipe(also known as recipe3
"""

import logging
import subprocess
from recipe import Recipe



class OverloadRecipe(Recipe):
    """
    This class implements recipe 3, which purposefully
    overload the services with 500 users.
    Load will stop after 15 minutes.
    """
    name = "recipe3"

    def get_name(self):
        return self.name
    
    def is_active(self):
        return True

    def break_service(self):
        """
        Call Locust load gen and create users' traffic that the cluster can't  handle.
        """
        logging.info("Overloading service with loadgen's users traffic")
        print("Breaking service operations...")
        Recipe._auth_cluster()
        overload_command = "kubectl set env deployment/loadgenerator LOCUST_TASK=break_locustfile.py"
        delete_pods_command = "kubectl delete pods -l app=loadgenerator"
        _, err_str = Recipe._run_command(overload_command)
        if "ERROR:" in str(err_str, "utf-8"):
            print(err_str)
            logging.error("Failed executing service breaking command:" + err_str)
        else:
            print("...done")
            logging.info('Loadgenerator deployed using overload pattern')
        _, err_str = Recipe._run_command(delete_pods_command)
        if "ERROR:" in str(err_str, "utf-8"):
            logging.error("Failed to delete loadgen overload pods:" + err_str)
        else:
            logging.info('Loadgenerator pods were deleted')


    def restore_service(self):
        """
        stop Load generating pods
        """
        print('Deploying working service...')
        Recipe._auth_cluster()
        
        _, err_str = Recipe._run_command(delete_pods_command)
        if "ERROR:" in str(err_str, "utf-8"):
            print(err_str)
            logging.error("Failed to restore service:" + err_str)
        else:
            print("service Restored")
            logging.info('Loadgenerator pods were deleted')


    def hint(self):
        """
        Provides a hint about finding the root cause of this recipe
        """
        print('Giving hint for recipe')
        get_project_command = "gcloud config list --format value(core.project)"
        project_id, error = Recipe._run_command(get_project_command)
        project_id = project_id.decode("utf-8").replace('"', '')
        if not project_id:
            print('No project ID found.')
            logging.error('No project ID found.')
            exit(1)
        print('Use Monitoring Dashboards to see metrics associated with GKE cluster and application services: https://console.cloud.google.com/monitoring/dashboards?project={}'.format(project_id))
        print('Note: It may take up to 5 minutes for monitoring metrics to be updated')

    def verify_broken_cause(self):
        """
        Displays a multiple choice quiz to the user about the cause of
        the breakage and prompts the user for an answer
        """
        prompt = 'What was the cause ?'
        choices = ['Too many requests', 'Requests were not parsed correctly', 'Ad service pod down', 'Recommendation service did not scale up']
        answer = 'Too many requests'
        Recipe._generate_multiple_choice(prompt.lower, choices, answer.lower())

    def verify(self):
        """Verifies the user found the root cause of the broken service"""
        print(
        '''
        This is a multiple choice quiz to verify that 
        you have found the root cause of the breakage.
        '''
            )
        self.verify_broken_cause()
        print(
        '''
        Good job! You have correctly identified which 
        service broke and what caused it to break.
        '''
            )
