pipeline {
    agent any
    stages {
        stage('Test') {
            agent {
                docker {
                    image 'python:3.8' 
                }
            }
            steps {
                echo 'Testing model correctness..'
                sh 'pip install -r requirements.txt'
            }
        }
        stage('deploy model serving'){
            agent {
                docker {
                    image 'python:3.9' 
                }
            }
            steps {
                echo 'Testing model serving..'
                sh 'make predictor_up'

            }
        }
        

    }
    
}