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

# Get argument as lowercase
ARGUMENT=$(echo "$1" | tr '[:upper:]' '[:lower:]')

if [ "${ARGUMENT}" == "start" ]; then
    # Get the current directory
    DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
    ROOT_DIR=$DIR/..
    cd $ROOT_DIR/docker/prod
    podman compose up --detach
elif [ "${ARGUMENT}" == "stop" ]; then
    # Get the current directory
    DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
    ROOT_DIR=$DIR/..
    cd $ROOT_DIR/docker/prod
    podman compose down
else
  echo "Usage: $0 <start|stop>"
  exit 1
fi