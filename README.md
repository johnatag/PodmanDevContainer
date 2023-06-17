# Features

The goal of this project is to provide a standard template for developping fullstack apps/microservices with observability in mind.
This template will provide:
- An already configured Observability platform using the OTEL Collector and the PromStack.
- A devcontainer configuration that should work with podman or docker out of the box
    - List of containers:
        - Python microservice (devcontainer)
        - PostgresSQL
        - Prometheus for metrics
        - Grafana for visualization
        - Jaegar for traces
        - Loki for logs
        - OTEL Collector
- An instrumented python microservice using the OpenTelemetry SDK/API (WIP)
- Swagger and OpenAPI 3.1 integration for documentation and testing (WIP)
- CI/CD configurations (WIP)
- Frontend React client (WIP)

**Important:** All of these configurations are for a local/dev environment. We would still need to properly configure an OTEL Collector/backends for production.

# Why use Podman instead of Docker
For security reasons, it is generally a good idea to do as much as possible on a standard user (non-administrator) without root access. Unfortunately, Docker requires root access in order to install/run properly on Mac OS which greatly increases the attack surface. Podman is a great alternative to docker since it's daemon-less, and it can operate without root by default.

However, due to it's rootless design, additional configuration is required to make it work with VSCode Devcontainers. Compared to Docker, you will encounter a lot more issues, bugs and broken things. 

\* Rootless Docker: I know that it exists, but I think at this point there's very little advantage using Rootless Docker compared to Podman

\* My environment is not the standard recommended one by HomeBrew, so I'm expecting more issues down the line

# Steps to reproduce the environment

0. Create a standard user without root access and set it up
1. Install Homebrew without root and update the PATH (usually not recommended)
```bash
# Git clone homebrew
git clone https://github.com/Homebrew/brew ~/.brew
# Add these two lines to your .zshrc file
export PATH="$HOME/.brew/bin:$HOME/.brew/sbin:$PATH"
export HOMEBREW_CASK_OPTS="--appdir=~/Applications"

# Usually Applications are installed in the /Applications folder which installs them system-wide, but I prefer to install them on a per-user basis.
```
2. Install and setup podman and podman-compose by following these [instructions](https://podman.io/docs/installation)
```bash
brew install podman
brew install podman-compose
podman machine init
podman machine start
```

3. Setup Visual Studio Code
- Install the [DevContainer](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers) and [Docker](https://marketplace.visualstudio.com/items?itemName=ms-azuretools.vscode-docker) extensions
- Configure Extensions:
    - Go to the Dev Containers extension settings
    - Change the Docker Executable path to "podman"
    - Change the Docker Compose path to "podman-compose"
    - Go to the Docker extension settings
Change the Docker Path to the absolute path to the Podman binary
Add the environment variable DOCKER_HOST with the value that points to the podman socket:
On a MacOS machine, you would give it the value: unix:///Users/$USER/.local/share/podman/podman-machine-default/podman.sock
```JSON
{
    "docker.dockerPath": "/Users/$USER/.brew/bin/podman",
    "docker.environment": {
        "DOCKER_HOST": "unix:///Users/$USER/.local/share/containers/podman/machine/qemu/podman.sock"
    },
    "dev.containers.dockerPath": "podman",
    "dev.containers.dockerComposePath": "podman-compose"
}
```

4. Setup the first devcontainer
- Make sure you set up Podman by running podman machine init and then podman machine start
- After making sure that Podman is ready to go, you need to create and/or open the project where you want to set up the development container.
- Using the Command Palette in Visual Studio Code, begin typing and select the option "Dev Containers: Add Dev Container Configuration Files..."
- Select your base image of choice
- Select any additional features to install inside the container and press "OK"
    - This will create a .devcontainer directory in your workspace that contains a devcontainer.json file. This file tells Visual Studio Code how to access or create your development container
- Next you need to make some modifications to the devcontainer.json file that is provided to you by the extension in order to get it working with Podman
    - On a MacOS machine, you need to add the following line:
        ```JSON
        "runArgs": ["--userns=keep-id:uid=1000,gid=1000"],
        "containerUser": "vscode",
        ```
- After making those modifications, you can run your first development container! Using the Command Palette in Visual Studio Code, begin typing and select the option "Dev Containers: Rebuild and Reopen in Container"
    - This will begin setting up your development container
    - Once the extension is done setting up your container, pull up the terminal and you can interact with the container! Feel free to create files and make changes to them.
- *IMPORTANT*: If instead of a base image, we want to use a Dockerfile/Containerfile, we need to create and select the user in the Dockerfile/Containerfile
    ```JSON
    devcontainer.json that works with podman on Mac OS
    {
        "name": "Alpine",
        "build": {
            "dockerfile": "Containerfile"
        },
        "runArgs": ["--userns=keep-id:uid=1000,gid=1000"],
        "containerUser": "vscode",
        "customizations": {
            "vscode": {
                "extensions": [
                    "ms-azuretools.vscode-docker"
                ]
            }
        }
    }
    ```

    ```Dockerfile
    # Containerfile

    FROM python:slim-bullseye
    RUN useradd -ms /bin/bash vscode
    USER vscode
    ```
- In our case, we are extending the usage to podman-compose
