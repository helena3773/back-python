pipeline {
    agent any

    options {
        disableConcurrentBuilds()
        timestamps()
    }

    parameters {
        string(name: 'IMAGE_TAG', defaultValue: '', description: 'Optional Docker image tag. Defaults to the Jenkins build number.')
        booleanParam(name: 'SKIP_SMOKE_TESTS', defaultValue: false, description: 'Skip running the container smoke tests stage.')
        booleanParam(name: 'PUSH_LATEST', defaultValue: true, description: 'Tag and push the image as `latest` in addition to the build tag.')
    }

    environment {
        // 컨테이너 이미지 이름(레지스트리 경로 제외)
        IMAGE_NAME = 'jyy1108u/flask-backend'
        // Docker Hub를 사용한다면 빈 문자열을 유지하고,
        // 프라이빗 레지스트리를 쓴다면 예: 'registry.my-company.com'
        DOCKER_REGISTRY_HOST = ''
        // 프라이빗 레지스트리 로그인 URL (예: 'https://registry.my-company.com')
        DOCKER_REGISTRY_URL = ''
        DOCKER_CREDENTIALS_ID = 'dockerhub-credentials'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Prepare build metadata') {
            steps {
                script {
                    env.EFFECTIVE_IMAGE_TAG = params.IMAGE_TAG?.trim() ? params.IMAGE_TAG.trim() : env.BUILD_NUMBER
                    def registryPrefix = env.DOCKER_REGISTRY_HOST?.trim() ? "${env.DOCKER_REGISTRY_HOST}/" : ''
                    env.IMAGE_URI = "${registryPrefix}${env.IMAGE_NAME}:${env.EFFECTIVE_IMAGE_TAG}"
                    env.LATEST_IMAGE_URI = "${registryPrefix}${env.IMAGE_NAME}:latest"
                }
            }
        }

        stage('Docker build') {
            steps {
                sh '''#!/bin/bash -eux
                docker build \
                  --file Dockerfile \
                  --tag "${IMAGE_URI}" \
                  .
                '''
            }
        }

        stage('Container smoke tests') {
            when {
                expression { return params.SKIP_SMOKE_TESTS == false }
            }
            steps {
                sh '''#!/bin/bash -eux
                docker run --rm \
                  -e FLASK_ENV=production \
                  -e PYTHONUNBUFFERED=1 \
                  "${IMAGE_URI}" \
                  python -m compileall app.py api
                '''
            }
        }

        stage('Push image') {
            steps {
                script {
                    def loginUrl = env.DOCKER_REGISTRY_HOST?.trim() ? env.DOCKER_REGISTRY_URL : ''
                    withDockerRegistry(credentialsId: env.DOCKER_CREDENTIALS_ID, url: loginUrl) {
                        sh "docker push ${IMAGE_URI}"
                    }
                }
            }
        }

        stage('Tag latest') {
            when {
                expression { return params.PUSH_LATEST == true }
            }
            steps {
                script {
                    sh "docker tag ${IMAGE_URI} ${LATEST_IMAGE_URI}"
                    def loginUrl = env.DOCKER_REGISTRY_HOST?.trim() ? env.DOCKER_REGISTRY_URL : ''
                    withDockerRegistry(credentialsId: env.DOCKER_CREDENTIALS_ID, url: loginUrl) {
                        sh "docker push ${LATEST_IMAGE_URI}"
                    }
                }
            }
        }
    }

    post {
        always {
            sh 'docker image prune --force'
        }
    }
}