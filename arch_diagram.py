from diagrams import Diagram, Edge
from diagrams.aws.compute import Lambda
from diagrams.aws.ml import Sagemaker, Transcribe
from diagrams.aws.storage import S3

with Diagram("Serverless Audio Summarisation", show=True):
    transcriptions = S3("transcriptions_bucket")
    recordings = S3("recordings_bucket")

    transcribe_lambda = Lambda("TranscribeLambda")
    summarise_lambda = Lambda("SummariseLambda")
    transcribe = Transcribe("transcribe")
    bedrock = Sagemaker("bedrock")

    audio_edge = Edge(label="audio file", color="brown")
    text_edge = Edge(label="text file", color="black")
    event_edge = Edge(label="event", color="blue")

    (
        recordings
        >> event_edge
        >> transcribe_lambda
        >> audio_edge
        >> transcribe
        >> text_edge
        >> transcriptions
    )
    (
        transcriptions
        >> event_edge
        >> summarise_lambda
        >> bedrock
        >> text_edge
        >> transcriptions
    )
