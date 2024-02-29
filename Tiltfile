# -*- mode: Python -*-

docker_build('foops-service', '.', dockerfile='.tilt/docker/Dockerfile_foops')
docker_build('metafair-service', '.', dockerfile='.tilt/docker/Dockerfile_metafair')
docker_build('fair-backend', './backend', dockerfile='.tilt/docker/Dockerfile_backend')
docker_build('fair-frontend', './frontend', dockerfile='.tilt/docker/Dockerfile_frontend')

k8s_yaml('.tilt/namespace.yaml')
k8s_yaml('.tilt/deployment-db.yaml')
k8s_yaml('.tilt/deployment-foops.yaml')
k8s_yaml('.tilt/deployment-metafair.yaml')
k8s_yaml('.tilt/deployment-backend.yaml')
k8s_yaml('.tilt/deployment-frontend.yaml')

k8s_resource('fair-db', port_forwards=['5400:5432'])
k8s_resource('fair-metafair', port_forwards=['4000:80'])
k8s_resource('fair-frontend', port_forwards=['8000:8000'])
