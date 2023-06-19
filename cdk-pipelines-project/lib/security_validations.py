from  aws_cdk import(
    pipelines,
    aws_codebuild,
    aws_iam,
)
class SecurityValidations():

    @property
    def unit_tests(self):
        return self._unit_tests
    @property
    def security(self):
        return self._security
    @property
    def linting(self):
        return self._linting

    def get_steps(self):
        return [self._linting, self._unit_tests, self._security]


    def __init__(self, **kwargs) -> None:
        self._linting = pipelines.CodeBuildStep('linting_bandit',
          install_commands=['pip install bandit'],
          commands=['bandit -r .']
        )

        self._unit_tests= pipelines.CodeBuildStep('UnitTest',
          install_commands= ['npm install -g aws-cdk','pip install -r requirements-dev.txt', 
                             'pytest --junit-xml=test-report.xml --cov-report=xml ', 'pytest --cov --cov-report=xml'],
          commands= ['pytest'],
          partial_build_spec=aws_codebuild.BuildSpec.from_object({
            'reports': {
              'coverage': {
                'files': ['./coverage.xml'],
                'file-format': 'COBERTURAXML'
              },
              'unittest': {
                'files': ['./test-report.xml'],
                'file-format': 'JUNITXML'
              }}
          }),
          role_policy_statements= [
            aws_iam.PolicyStatement(
            actions= [
                'codebuild:CreateReportGroup',
                'codebuild:CreateReport',
                'codebuild:UpdateReport',
                'codebuild:BatchPutTestCases',
                'codebuild:BatchPutCodeCoverages'
              ],
              resources= ['*']
            )]
        )

        self._security = pipelines.CodeBuildStep('Security',
          install_commands= ['make warming','gem install cfn-nag'],
          commands= ['make build','make security'],
          partial_build_spec= aws_codebuild.BuildSpec.from_object({
            'phases': {
              'install': {
                'runtime-versions': {
                  'ruby': '2.6'
                }
              }
            }
          })
          )


