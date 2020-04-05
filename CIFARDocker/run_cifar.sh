# docker rm veh_docker
docker run -it -d --runtime=nvidia --name=cifar_docker_container -v /home/himanshu/Himanshu/Blog/CIFARDocker:/home/CIFARDocker --network=host docker_containerized_cifar