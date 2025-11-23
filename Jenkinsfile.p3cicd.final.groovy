pipeline {
    agent any
    
    environment {
        LOCAL_REPO_PATH = 'https://github.com/gregofh/unir-cicd'
        EMAIL_RECIPIENT = 'gregofh@gmail.com'
        TEST_API_URL = 'http://apiserver:5000'
    }
    // 1. Checkout
    stages {
        stage('checkout') {
            steps {
                cleanWs()
                echo '--- Checkout del Código ---'
                sh "git clone ${LOCAL_REPO_PATH} ."
            }
        }
        // 1. Build
        stage('Build') {
            steps {
                echo '--- Build de la aplicación ---'
                sh "make build"
            }
        }
        // 3. Unit Tests
        stage('Tests Unitarios') {
            steps {
                echo '--- Ejecutando Tests Unitarios  ---'
                sh 'make test-unit'
                archiveArtifacts artifacts: 'results/*.xml'
            }
        }
        // 4. API Tests
        stage('Tests de API') {
            steps {
                echo '--- Ejecutando Unit de API ---'
                sh 'make test-api BASE_URL=${TEST_API_URL}'
                archiveArtifacts artifacts: 'results/*.xml'
            }
        }
        // 5. E2E Tests
        stage('Tests E2E') {
            steps {
                echo '--- Ejecutando Tests E2E ---'
                sh 'make test-e2e'
                archiveArtifacts artifacts: 'results/*.xml'
            }
        }
        
    }
    post {
        always {
            // Procesamos los reportes generados
            junit 'results/*.xml'
            
            // 2. Reporte HTML bonito (Requiere plugin HTML Publisher)
            publishHTML(target: [
                reportDir: 'results',
                reportFiles: '*.html',
                reportName: 'Reporte Visual HTML'
            ])

            // 3. Gráfica de Cobertura
            recordCoverage(tools: [[parser: 'COBERTURA', pattern: 'results/coverage.xml']])       
            
            cleanWs()
        }
        failure {
            echo 'Enviando notificación de fallo por correo...'
            // Paso 'mail' del Email Extension Plugin
            mail(
                to: 'gregofh@gmail.com',
                subject: "🚨 FALLO CRÍTICO: ${env.JOB_NAME} - Ejecución #${env.BUILD_NUMBER}",
                body: """
                    El trabajo de Jenkins '${env.JOB_NAME}' ha fallado.
                    
                    Número de Ejecución: #${env.BUILD_NUMBER}
                    
                    Revisa los detalles y el log en el siguiente enlace:
                    ${env.BUILD_URL}
                    
                    ---
                    (Este es un mensaje automático de Jenkins)
                """.stripIndent()
            )
        }            
    }
}