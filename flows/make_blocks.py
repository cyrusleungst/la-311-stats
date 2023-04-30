from prefect_gcp.cloud_storage import GcsBucket
from prefect_gcp import GcpCredentials

service_account_info = {
    "type": "service_account",
    "project_id": "rare-deployment-385022",
    "private_key_id": "f1d40921c58966ccbc0cf2e1f40c3e6233cde6c4",
    "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQDfAZ7QHyt9EW7k\n7/TPv0evshM+RQeC15bEhdnIEKH/4+8hyM9R971QGdZOyTQrIHdvgBQRfOpx+qoz\njEIwHKNUjZuY07XPNc8JYSX62Pvhy3Ia2sB3FbabtuHsa0w8uFUVdo+HMuk/YvCt\nes+LvNGWB4BMS66N9yIlXQjbpOS1q3oAv8lIfYYe9h9r1rdrkrS85R/vQVqYlodM\naMHAGIz6MuTc5N8ijSZ3qbLJ6gmKGtSgMyRE/iP+QzKWexVBe2ZfZptc3XYfDI2H\nOONCU+vaEX1NdmjxAycVUkrncIX/a0WfCnmiShBlSyjd0sX+izHAqrt5z6GcERe8\n/M0TorhBAgMBAAECggEAFAVK4w0OqXF0OZIgB2VOeUPicw0IH0NdohJmOo42Yl5t\n7I7hAKSI1sp1sVMM9PDlksQL3oS5bjbT1Zbk+6Qb4bkThq/oZaGYub3YBreOPXeM\nrJkw/ZVHH0msP2kOn3DpFT6J+i2kP8WRLUdA9Mmkg0n0cbplrGcge1GT5wGHFZa+\n5bdg2p1yZ70aPisEshiDO1JxpdmnKlje4bFuStFQsl2BJvRwHjxM27R+cNzQtzqd\n3Xo+dMANe7LWYSySjnclrAZjwS5BMks6n73cwntgl6/+WwSPUNGO4uAeS7uPlvYc\nbxGLL/D37tWV9SZqaJvVlgiAf9lQ0MKYETJIPPgalQKBgQDyJuTdEs84ysGRBLoS\nQsVJkIz1gqzE9W4IDxCi2lwV29BU1B6wORFIJMP2A0nkE1bBWWQRpW+0RfyxIgNd\n+KMIe+r9xYSSut9BwUprOmSmI4oSJBJtGzSv5iAOO+JZVobRRq8EfVfSD4TwFdCk\nyexLP7rQQCb+tcJyz2yTaKVP+wKBgQDrwm9EmAevkSuM6WKDm6Vf+9g0CqeZC67N\npk5ykkWDy0k/Azy3cm+fnFtAmLYJLilr0OBzY/COcuuq1S23eLC8xuxF9zbnoaco\nSNjo0txT3ZNhznUvTk505yhS3erhfqgs79xs6g454GeNb0257PLd5PanflN1Mi+S\nJ7ivd+TX8wKBgAFO2HmhOmFSJw2DewXSOoKVN020MP63XKrKegqHJ2wuzcdHhgrp\npABBwpU3m1SSDivpMbMus5XDswO57U66oxbOpIxOXtL0E3SleKNvo0+KbZp/e2H/\nfZ9dnNq21BgrcXr76MIbczf9QXiShZf+Rzp406eAUTWbAbvhBvMc45e1AoGBALlO\ngpavyJq+yDRh3QUE+d+P3EhLd6BcBnGuHkr/nZQR3Oiiar7mO8aA51jGr45XskcE\nTudjzlipC4OjO+PSAVjgIiZ8QbOe4/xOBfA6jON+bbGazZD5Q8GvT4qS02OaYiWw\nAtm4vqXPNJV+vuE81UiEBztvl7muUKXYgtmoqz7xAoGAMs7dy5hA+lNd3nMxOUqj\nqgP2K/cLgAFZ5zKBURsIYoO/3HWd/ZTxAkhkuPK6nM9qzgJc89w8yhx/fZOhmdte\n8CtdgkW/zG6f75sRjjxaX4k6nyeMIOmVw/1sUJH6sfoEk17bI9EMUaqb4sPiMKyL\nefdr5NWustKsMNY9IY8gUu4=\n-----END PRIVATE KEY-----\n",
    "client_email": "de-user@rare-deployment-385022.iam.gserviceaccount.com",
    "client_id": "103523871901744158383",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/de-user%40rare-deployment-385022.iam.gserviceaccount.com"
}

print("Creating GCP credentials block")
GcpCredentials(
    service_account_info=service_account_info
).save("divvy-trips-creds", overwrite=True)

print("Creating GCS bucket block")
GcsBucket(
    bucket="la_311",
    gcp_credentials=GcpCredentials.load("divvy-trips-creds")
).save("divvy-trips-gcs", overwrite=True)
