# A.M.A

## How To

<details><summary>setup</summary>

```bash
docker build -t ama:lightsail . -f ./Dockerfile.aws.lightsail

cp .env.sample .env

docker container run --rm \
    -v `pwd`/app:/app \
    -v $HOME/.aws:/root/.aws \
    --env-file .env \
    -p 8000:8000 \
    ama:lightsail --reload
```

</details>