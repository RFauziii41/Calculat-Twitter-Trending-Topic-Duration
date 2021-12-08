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
| No | topic | country | woeid | duration |
| -- | ----- | ------- | ----- | -------- |
1 | #B430TS1 | Singapore | 23424948 | 40.0 |
2 | #B430TS1 | Thailand | 23424960 | 19.0 |
3 | #ELEVEN1stWin | Indonesia | 23424846 | 149.0 |
4 | ELEVEN1stWin | Malaysia | 23424901 | 133.0 |
5 | #ELEVEN1stWin | Philippines | 23424934 | 140.0 |
6 | #ELEVEN1stWin | Singapore | 23424948 | 80.0 |
7 | #Hawkeye | Indonesia | 23424846 | 5.0 |
8 | #IVE1stWin | Malaysia | 23424901 | 5.0 |
9 | #IVE1stWin | Philippines | 23424934 | 9.0 |
10 | #IVE1stWin | Singapore | 23424948 | 4.0 |
11 | #IVE1stwin | Malaysia | 23424901 | 9.0 |
12 | #InovasiTelkomIndofarma | Indonesia | 23424846 | 65.0 |
13 | Lazada1212XBrightWin | Thailand | 23424960 | 115.0 |
14 | #TRUZMentionParty | Indonesia | 23424846 | 4.0 |
15 | #kookv | Thailand | 23424960 | 24.0 |
16 | #แบนSITALA | Thailand | 23424960 | 240.0 |
17 | AYATO | Indonesia | 23424846 | 15.0 |
18 | AYATO | Malaysia | 23424901 | 10.0 |
19 | AYATO | Philippines | 23424934 | 10.0 |
20 | AYATO | Singapore | 23424948 | 15.0 |
21 | Ayato | Indonesia | 23424846 | 60.0 |
22 | Ayato | Malaysia | 23424901 | 110.0 |
23 | Ayato | Philippines | 23424934 | 55.0 |
24 | Ayato | Singapore | 23424948 | 233.0 |
25 | TAEKOOK | Indonesia | 23424846 | 89.0 |
26 | TAEKOOK | Malaysia | 23424901 | 79.0 |
27 | TAEKOOK | Philippines | 23424934 | 113.0 |
28 | Taekook | Malaysia | 23424901 | 5.0 |
29 | ayato | Singapore | 23424948 | 5.0 |
30 | taekook |  Indonesia | 23424846 | 10.0 |
31 | taekook | Philippines | 23424934 | 70.0 |
33 | taekook | Singapore | 23424948 | 20.0 |

> Hasil yang ditampilan merupakan program yang diekseskui pada tanggal 08 Desember 2021 Pukul 12.15 WIB hingga 08 Desember 2021 Pukul 19.00 WIB
