import aws_cdk as cdk
from RIVStack import RIVStack

app = cdk.App()
RIVStack(app, "RIVStack")
app.synth()