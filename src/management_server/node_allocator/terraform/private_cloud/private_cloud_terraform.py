import subprocess
import time
import json
import os
import re
from utils import get_logger, format_terraform_error_message, run_subprocess_cmd

current_dir = os.getcwd()
terraform_dir = os.path.join(current_dir, "node_allocator", "terraform", "private_cloud")

logger = get_logger(terraform_dir, log_file="private_cloud_terraform.log")
    
# Destroy private cloud
async def destroy_private_cloud():
    try:
        # Destroy resources
        run_subprocess_cmd(["terraform", "destroy", "-auto-approve", "-var-file=private.tfvars"], cwd=terraform_dir, logger=logger)
        logger.info("Private cloud destroyed")
        return {"message": "Private cloud destroyed", "status": "success"}
    
    except subprocess.CalledProcessError as e:
        # Log the error message and return it
        error_message = e.output.decode("utf-8")
        print(error_message)
        error_message = format_terraform_error_message(error_message)
        logger.error(error_message)
        return {"error_message": error_message, "status": "failed"}
    
    except  Exception as e:
        return {"error_message": str(e), "status": "failed"}
    

# Destroy and provision private cloud
async def destroy_and_provision_private_cloud():
    try:
        # Destroy resources
        run_subprocess_cmd(["terraform", "destroy", "-auto-approve", "-var-file=private.tfvars"], cwd=terraform_dir, logger=logger)
        
        # Initialize Terraform
        run_subprocess_cmd(["terraform", "init"])
        
        # Apply terraform
        await apply_terraform()
        
        logger.info("Destroy and provisioning completed")
        return {"message": "Destroy and provisioning completed", "status": "success"}
    
    except subprocess.CalledProcessError as e:
        # Log the error message and return it
        error_message = e.output.decode("utf-8")
        print(error_message)
        error_message = format_terraform_error_message(error_message)
        logger.error(error_message)
        return {"error_message": error_message, "status": "failed"}
    
    except  Exception as e:
        return {"error_message": str(e), "status": "failed"}
    
    
# Initialize Terraform and apply changes
async def provision_private_cloud():  
    try:  
        # Initialize Terraform
        subprocess.run(["terraform", "init"], cwd=terraform_dir, logger=logger)
        await apply_terraform()
        
        logger.info("Private cloud provisioned")
        return {"message": "Private cloud provisioned", "status": "success"}
    
    except subprocess.CalledProcessError as e:
        # Log the error message and return it
        error_message = e.output.decode("utf-8")
        print(error_message)
        error_message = format_terraform_error_message(error_message)
        logger.error(error_message)
        return {"error_message": error_message, "status": "failed"}
    
    except  Exception as e:
        return {"error_message": str(e), "status": "failed"}

# Apply changes
async def apply_private_cloud():
    try:
        await apply_terraform()
        logger.info("Private cloud changes applied")
        return {"message": "Private cloud changes applied", "status": "success"}
    
    except subprocess.CalledProcessError as e:
        # Log the error message and return it
        error_message = e.output.decode("utf-8")
        print(error_message)
        error_message = format_terraform_error_message(error_message)
        logger.error(error_message)
        return {"error_message": error_message, "status": "failed"}
    
    except  Exception as e:
        return {"error_message": str(e), "status": "failed"}

# Private function to apply changes
async def apply_terraform():
    try:
        # Apply changes
        run_subprocess_cmd(["terraform", "apply", "-auto-approve", "-var-file=private.tfvars"], cwd=terraform_dir, logger=logger)
        
        # Wait for instances to be provisioned
        time.sleep(60)
        
        # Save Terraform output to a JSON file
        output = run_subprocess_cmd(["terraform", "output", "-json"], cwd=terraform_dir, logger=logger)
        print(output)
        with open(f"{terraform_dir}/private_instance_terraform_output.json", "w") as f:
            f.write(output)
            
    except subprocess.CalledProcessError as e:
        # Log the error message and return it
        error_message = e.output.decode("utf-8")
        print(error_message)
        error_message = format_terraform_error_message(error_message)
        logger.error(error_message)
        return {"error_message": error_message, "status": "failed"}
    
    except  Exception as e:
        return {"error_message": str(e), "status": "failed"}
    