# Serendipity Docs

## Installations & Setup

1. Create a `.env` file with all the contents of the .env.sample for local-development
1. Load questions fixtures with the following command

   ```shell
   py manage.py loaddata checkins/fixtures/checkin-app.json
   ```

## API References

API documentation available in the following formats:

- [Swagger](http://127.0.0.1:8000/api/docs/swagger/) or when deployed at api/docs/swagger/
- [Redoc](http://127.0.0.1:8000/api/docs/redoc/) or when deployed at api/docs/redoc/

Note:

- API authentication for login will accept either a username string or email under the key of username in the request body

```js
{
    "username": "something@gmail.com",
    "password": "1234_asdf"
}

// or

{
    "username": "something",
    "password": "1234_asdf"
}
```
