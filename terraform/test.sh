project_id="my project"
bucket_name="my bucket"
billing_id="billing"

terraform_command = "echo apply -auto-approve -var="project_id="${project_id}"" -var="bucket_name="${bucket_name}"" -var="skip_loadgen=${skip_loadgen:-false}""
#If billing account provided specify it 
if [[ -n "$billing_id" ]]; then
    terraform_command += "-var="billing_account=${billing_acct}"" 
fi

#check if new installtion or if cluster already and what is the version
gke_location="$(gcloud container clusters list --format="value(location)" --filter name=cloud-ops-sandbox)"
if [[ -n "$gke_location" ]]; then 
    echo "gke_location"
    gke_version="$(gcloud container clusters describe cloud-ops-sandbox --region "${gke_location}"  --format="value(resourceLabels.version)")"
    echo "gke_version"
fi
#If cluster exist and it's older version use backward comp. params
if [[ -n "$gke_location"  || -z "$gke_version" ]]; then 
    terraform_command+="-var="gke_node_count=4" -var="loadgen_node_count=2" --var="app_version="pre""
else
    terraform_command+="--var="app_version=${app_ver}"" 
fi 

echo $terraform_command
eval "$terraform_command"