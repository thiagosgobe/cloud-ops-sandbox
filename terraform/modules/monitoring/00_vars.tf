/**
 * Copyright 2020 Google LLC
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *      http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

variable "zone" {
  type        = string
  description = "GKE cluser zone, needed for istio services monitoring. Can be revealed by running \"gcloud container clusters list --filter='name:cloud-ops-sandbox' --project $project_id --format='value(zone)')\" from Google Cloud CLI"
}

variable "external_ip" {
  type        = string
  description = "The external IP of the frontend cluster. Can be revealed by running \"kubectl get service frontend-external'\" in the Google Cloud CLI."
}


variable "project_id" {
  type        = string
  description = "The id of your project. Case-sensitive."
}

variable "account_email" {
  type        = string
  description = "The account email. ."
}


variable "services" {
  type = list(object({
    service_name = string,
    service_id   = string
  }))
  default = [
    {
      service_name = "Payment Service"
      service_id   = "paymentservice"
    },
    {
      service_name = "Email Service"
      service_id   = "emailservice"
    },
    {
      service_name = "Shipping Service"
      service_id   = "shippingservice"
    }
  ]
}