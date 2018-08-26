from background_task import background


@background(schedule=10)
def notify():
    # lookup user by id and send them a message
    print("Hello world!")
