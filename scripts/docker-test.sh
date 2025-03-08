if [ -z "$1" ]; then
  echo "Usage: $0 <start|stop>"
  exit 1
fi

# Check if podman is installed
if ! command -v podman &> /dev/null
then
    echo "podman could not be found"
    exit
fi

# Check if podman machine is running
if ! podman info &> /dev/null
then
    echo "podman machine is not running"
    exit
fi

CURRENT_DIR=$(pwd)

# Get argument as lowercase
ARGUMENT=$(echo "$1" | tr '[:upper:]' '[:lower:]')

if [ "${ARGUMENT}" == "start" ]; then
    # Get the current directory
    DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
    # remove any existing containers for api and client
    if podman ps -a | grep -q "api"; then
        podman rm -f api
    fi
    if podman ps -a | grep -q "client"; then
        podman rm -f client
    fi
    ROOT_DIR=$DIR/..
    cd $ROOT_DIR/docker/test
    podman compose down
    DB_PASSWORD="example" podman compose up -d
elif [ "${ARGUMENT}" == "stop" ]; then
    # Get the current directory
    DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
    ROOT_DIR=$DIR/..
    cd $ROOT_DIR/docker/test
    podman compose down
else
  echo "Usage: $0 <start|stop>"
  exit 1
fi

cd $CURRENT_DIR