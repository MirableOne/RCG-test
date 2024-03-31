## Requirements

* docker-compose

## Notes

To reduce work time I didn't add a migration setup. DB schema could be found at `schema/schema.sql`

## Setup

```shell
cp .env.dist .env
```

Replace `<YOUR-API-TOKEN>` with actual one.

```shell
docker-compose up -d database
```

Run schema query.

## Run

```shell
docker-compose up app --build
```