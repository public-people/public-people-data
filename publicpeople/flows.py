from viewflow import flow
from viewflow.base import this, Flow
from viewflow.flow.views import CreateProcessView, UpdateProcessView

from .models import HelloWorldProcess

from viewflow import frontend


@frontend.register
class HelloWorldFlow(Flow):
    process_class = HelloWorldProcess

    start = (
        flow.Start(
            CreateProcessView,
            fields=["text"]
        ).Permission(
            auto_create=True
        ).Next(this.approve)
    )

    approve = (
        flow.View(
            UpdateProcessView,
            fields=["text", "approved"]
        ).Permission(
            auto_create=True
        ).Next(this.check_approve)
    )

    check_approve = (
        flow.If(lambda activation: activation.process.approved)
        .Then(this.send)
        .Else(this.fix)
    )

    fix = (
        flow.View(
            UpdateProcessView,
            fields=["text"]
        ).Permission(
            auto_create=True
        ).Next(this.check_approve)
    )

    send = (
        flow.Handler(
            this.send_hello_world_request
        ).Next(this.end)
    )

    end = flow.End()

    def send_hello_world_request(self, activation):
        print(activation.process.text)
