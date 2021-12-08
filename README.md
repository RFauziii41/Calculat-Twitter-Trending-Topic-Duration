# Pengantar
Program yang dibuat merupakan program untuk menghitung berapa lama suatu topik dapat bertahan di posisi yang paling trending dari beberapa negara di asia tenggara. Trending topik yang diambil hanya topik yang teratas (paling trending) di masing-masing negara.

## Proses Pengambilan Data
Pengambilan data (data trending) menggunakan library yang tersedia pada Python, yaitu "tweepy". Pada libary tersebut dibutuhkan API Key & Access Token yang dapat digenerate pada Twitter Developer Platform.

## Proses Perhitungan Trending Terlama
Terdapat 2 task yang di-set pada program ini. Task pertama melakukan pengambilan data pada Twitter, kemudian disimpan ke dalam database. Task kedua melakukan pengambilan data pada database untuk menghitung durasinya. Kedua task tersebut akan dieksekusi setiap 5 menit, tools yang digunakan untuk mengatasi scheduler tersebut adalah Apache Airflow. Hasil durasi trending topik akan ditampilkan pada logs Airflow.

# Library
Berikut library-library yang digunakan pada program ini.
| Library | Kebutuhan |
| :------ | --------- |
| `pandas` | menyimpan data sebagai DataFrame dan melakukan perhitungan durasi trending |
| `tweepy` | mengambil data trending dari aplikasi Twitter |
| `sqlalchemy.create_engine` | menghubungkan database supaya dapat berkomunikasi dengan database melalui program yang dibuat |
| `datetime.datetime` | membuat format datetime pada `start_date` di `default_args` pada saat membuat DAG |
| `airflow.models.DAG` | membuat DAG pada Airflow |
| `airflow.models.Variable` | memanggil variable yang dibuat pada Airflow |
| `airflow.operators.python_operator.PythonOperator` | membuat task yang dibuat dalam program Python |

# Hasil
| topic | country | woeid | duration |
| ----- | ------- | ----- | -------- |

> Hasil yang ditampilan merupakan program yang diekseskui pada tanggal 08 Desember 2021 Pukul 12.15 WIB hingga 08 Desember 2021 Pukul xx.xx WIB
