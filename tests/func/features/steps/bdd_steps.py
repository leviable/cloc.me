from behave import when, then

CONTAINER_TIMEOUT = 30


@when('I run the clocme container')
def call_clocme_container(context):
    docker = context.docker
    image = context.image_name
    context.container = docker.containers.run(image, '--help', detach=True)


@then('the container completes')
def clocme_container_completes(context):
    context.container.wait(timeout=CONTAINER_TIMEOUT)


@then('the container exits with "{exp_status}" status')
def clocme_container_exits(context, exp_status):
    container = context.container
    container.reload()
    act_status = container.status

    msg = f"Expected status of {exp_status}, found {act_status}"
    assert exp_status == act_status, msg
