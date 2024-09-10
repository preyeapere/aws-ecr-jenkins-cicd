#Go to the AWS dashboard and then to the EC2 services. create an instance
#After the successful SSH connection, firstly update the Linux machine. And install java using below commands:
sudo apt update
sudo apt install openjdk-17-jre
java -version

#Lets install jenkins using below commands
curl -fsSL https://pkg.jenkins.io/debian/jenkins.io-2023.key | sudo tee \
/usr/share/keyrings/jenkins-keyring.asc > /dev/null
echo deb [signed-by=/usr/share/keyrings/jenkins-keyring.asc] \
https://pkg.jenkins.io/debian binary/ | sudo tee \
/etc/apt/sources.list.d/jenkins.list > /dev/null
sudo apt-get update
sudo apt-get install jenkins

#You can enable the Jenkins service to start at boot with the command
sudo systemctl enable jenkins
sudo systemctl start jenkins
sudo systemctl status jenkins

#sudo apt install git

#Access Jenkins on Browser
https//:<Instance_ip>:8080

#After that On the browser, you should see the Jenkins interface that asks for the administrator password.
Now cat the following Jenkins file to retrieve the Administrator password and paste it to the Jenkins dashboard.

Here, create a Jenkins user

After the configuration is completed, you should see the Jenkins dashboard.

#We may also set up AWS credentials in Jenkins so that it facilitates the Docker push to the ECR repository.

GO to the Manage Jenkins>>Credentials>>system>>Global credentials
Then add credentials and here add AWS username and password and account ID

#Now here we need to Install Docker
sudo apt  install docker.io

After Installing Docker we need to give some permission
sudo usermod -aG docker $USER
sudo chmod 666 /var/run/docker.sock

After installing docker lets Restart jenkins
sudo systemclt restart jenkins

Go to the manage Jenkins>>Plugins>>Available Plugin

Docker
Docker Pipeline
Amazon ECR plugin

#Lets Create AWS ECR repository to push this image so Go to AWS ECR repository and create

#Here in this step we need to create IAM role with below permission 

Attach permission policies : AmazonEC2ContainerRegistryFullAccess

#Install AWS CLI on Ubuntu 22.04 LTS
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip 
sudo ./aws/install

#Push Docker image to AWS ECR using Jenkins pipeline

So lets create jenkins pipeline go to the Jenkins Dashboard Click on new Item select Pipeline and paste this code

pipeline {
    agent any
    environment {
        AWS_ACCOUNT_ID="222222222222"
        AWS_DEFAULT_REGION="us-east-1"
        IMAGE_REPO_NAME="jenkins-pipeline"
        IMAGE_TAG="v1"
        REPOSITORY_URI = "22222222222.dkr.ecr.us-east-1.amazonaws.com/jenkins-pipeline"
    }
   
    stages {
        
         stage('Logging into AWS ECR') {
            steps {
                script {
                sh """aws ecr get-login-password --region ${AWS_DEFAULT_REGION} | docker login --username AWS --password-stdin ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_DEFAULT_REGION}.amazonaws.com"""
                }
                 
            }
        }
        
        stage('Cloning Git') {
            steps {
                checkout([$class: 'GitSCM', branches: [[name: '*/master']], doGenerateSubmoduleConfigurations: false, extensions: [], submoduleCfg: [], userRemoteConfigs: [[credentialsId: '', url: 'https://github.com/sd031/aws_codebuild_codedeploy_nodeJs_demo.git']]])     
            }
        }
  
    // Building Docker images
    stage('Building image') {
      steps{
        script {
          dockerImage = docker.build "${IMAGE_REPO_NAME}:${IMAGE_TAG}"
        }
      }
    }
   
    // Uploading Docker images into AWS ECR
    stage('Pushing to ECR') {
     steps{  
         script {
                sh """docker tag ${IMAGE_REPO_NAME}:${IMAGE_TAG} ${REPOSITORY_URI}:$IMAGE_TAG"""
                sh """docker push ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_DEFAULT_REGION}.amazonaws.com/${IMAGE_REPO_NAME}:${IMAGE_TAG}"""
         }
        }
      }
    }
}

Now lets Check ECR Repo our image push or not

Conclusion:

In this article we have covered Configuring EC2 instance in AWS,  Install Java on  Ubuntu 22.04 LTS, Install Jenkins on Ubuntu 22.04 LTS, Add AWS credentials in Jenkins, Creating ECR Repository in AWS, Create AmazonEC2ContainerRegistryFullAccess IAM Role in AWS, how to Build and Push Docker image to AWS ECR using Jenkins pipeline.