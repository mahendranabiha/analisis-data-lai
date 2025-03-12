import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import seaborn as sns
import streamlit as st


# Konfigurasi page
st.set_page_config(layout="wide", initial_sidebar_state="expanded")


# Konfigurasi sidebar
# Baris pertama
st.sidebar.title("Analisis Bike Sharing `oleh Mahendra`")
st.sidebar.header("Parameter", divider=True)

# Baris kedua
st.sidebar.subheader("Jumlah Penyewaan Sepeda per Bulan")
plot_year = st.sidebar.multiselect("Pilih Tahun", [2011, 2012])

# Baris ketiga
st.sidebar.markdown(
    """
    ---
    Laskar AI - 2025
    """
)


# Helper function untuk hasil analisis yang akan divisualisasikan
# Deklarasi variabel untuk dataframe utama
df_main = pd.read_csv("main_data.csv")


# Function untuk penyesuaian input multiselect dengan output visualisasi jumlah penyewaan sepeda per bulan
def status_year(df, plot):
    try:
        if plot[0] == 2011 and plot[1] == 2012:
            # Apabila pilihan tahun 2011 dan 2012
            for index, value in df["yr"].items():
                if value == 0:
                    # Apabila data bernilai 0
                    df.iloc[index, 3] = 2011
                elif value == 1:
                    # Apabila data bernilai 1
                    df.iloc[index, 3] = 2012
            return df
        elif plot[1] == 2011 and plot[0] == 2012:
            # Apabila pilihan tahun 2012 dan 2011
            for index, value in df["yr"].items():
                if value == 0:
                    # Apabila data bernilai 0
                    df.iloc[index, 3] = 2011
                elif value == 1:
                    # Apabila data bernilai 1
                    df.iloc[index, 3] = 2012
            return df

    except IndexError:
        if plot[0] == 2011:
            # Apabila pilihan hanya tahun 2011
            for index, value in df["yr"].items():
                if value == 0:
                    # Apabila data bernilai 0
                    df.iloc[index, 3] = 2011
                elif value == 1:
                    # Apabila data bernilai 1
                    df.iloc[index, 3] = 1
            df = df.drop(df.loc[(df["yr"] == 1)].index, axis=0)
            return df

        elif plot[0] == 2012:
            # Apabila pilihan hanya tahun 2012
            for index, value in df["yr"].items():
                if value == 1:
                    # Apabila data bernilai 1
                    df.iloc[index, 3] = 2012
                elif value == 0:
                    # Apabila data bernilai 0
                    df.iloc[index, 3] = 0
            df = df.drop(df.loc[(df["yr"] == 0)].index, axis=0)
            return df


# Eksekusi function status_year pada dataframe utama
try:
    df_main = status_year(df_main, plot_year)

except IndexError:
    for index, value in df_main["yr"].items():
        if value == 0:
            # Apabila data bernilai 0
            df_main.iloc[index, 3] = 2011
        elif value == 1:
            # Apabila data bernilai 1
            df_main.iloc[index, 3] = 2012


# Function untuk jumlah penyewaan sepeda per bulan
def create_trends_bike_rental(df):
    trends_bike_rental = df.groupby(["yr", "mnth"])[["cnt"]].agg({"cnt": "sum"})
    trends_bike_rental = trends_bike_rental.reset_index()

    return trends_bike_rental


# Function untuk pengkategorian data season
def cluster_season(x):
    if x == 1:
        # Apabila data bernilai 1
        return "Semi"
    elif x == 2:
        # Apabila data bernilai 2
        return "Panas"
    elif x == 3:
        # Apabila data bernilai 3
        return "Gugur"
    elif x == 4:
        # Apabila data bernilai 4
        return "Dingin"
    else:
        # Apabila data selain bernilai 1, 2, 3, atau 4
        pass


# Function untuk season dengan jumlah pelanggan paling banyak yang belum mendaftar
def create_most_season_bycasual(df):
    most_season_bycasual = df.groupby(["season"])[["casual"]].agg({"casual": "sum"})
    most_season_bycasual = most_season_bycasual.reset_index()

    # Apply kolom season untuk mengubah nilai pengkategorian numerik menjadi kategorik
    most_season_bycasual["season"] = most_season_bycasual["season"].apply(
        lambda x: cluster_season(x)
    )

    # Sort value berdasarkan jumlah pelanggan yang telah mendaftar atau yang belum mendaftar
    most_season_bycasual = most_season_bycasual.sort_values(
        by="casual", ascending=False
    )

    return most_season_bycasual


# Function untuk season dengan jumlah pelanggan paling banyak yang telah mendaftar
def create_most_season_byregistered(df):
    most_season_byregistered = df.groupby(["season"])[["registered"]].agg(
        {"registered": "sum"}
    )
    most_season_byregistered = most_season_byregistered.reset_index()

    # Apply kolom season untuk mengubah nilai pengkategorian numerik menjadi kategorik
    most_season_byregistered["season"] = most_season_byregistered["season"].apply(
        lambda x: cluster_season(x)
    )

    # Sort value berdasarkan jumlah pelanggan yang telah mendaftar atau yang telah mendaftar
    most_season_byregistered = most_season_byregistered.sort_values(
        by="registered", ascending=False
    )

    return most_season_byregistered


# Function untuk jam-jam dengan jumlah penyewaan sepeda paling banyak pada saat holiday
def create_most_hours_byholiday(df):
    most_hours_byholiday = (
        df.groupby(["holiday", "hr"])[["cnt"]]
        .agg({"cnt": "sum"})
        .sort_values(by="cnt", ascending=False)
    )
    most_hours_byholiday = (
        most_hours_byholiday.loc[(1, slice(None)), :]
        .head(8)
        .sort_values(by="hr", ascending=True)
    )
    most_hours_byholiday = most_hours_byholiday.reset_index()

    return most_hours_byholiday


# Function untuk jam-jam dengan jumlah penyewaan sepeda paling banyak pada saat weekend
def create_most_hours_byweekend(df):
    most_hours_byweekend = (
        df.groupby(["weekend", "hr"])[["cnt"]]
        .agg({"cnt": "sum"})
        .sort_values(by="cnt", ascending=False)
    )
    most_hours_byweekend = (
        most_hours_byweekend.loc[(1, slice(None)), :]
        .head(8)
        .sort_values(by="hr", ascending=True)
    )
    most_hours_byweekend = most_hours_byweekend.reset_index()

    return most_hours_byweekend


# Function untuk jam-jam dengan jumlah penyewaan sepeda paling banyak pada saat workingday
def create_most_hours_byworkingday(df):
    most_hours_byworkingday = (
        df.groupby(["workingday", "hr"])[["cnt"]]
        .agg({"cnt": "sum"})
        .sort_values(by="cnt", ascending=False)
    )
    most_hours_byworkingday = (
        most_hours_byworkingday.loc[(1, slice(None)), :]
        .head(8)
        .sort_values(by="hr", ascending=True)
    )
    most_hours_byworkingday = most_hours_byworkingday.reset_index()

    return most_hours_byworkingday


# Konfigurasi main page
# Deklarasi variabel untuk dataframe hasil analisis yang akan divisualisasikan
df_bike_rental = create_trends_bike_rental(df_main)
df_bycasual = create_most_season_bycasual(df_main)
df_byregistered = create_most_season_byregistered(df_main)
df_byholiday = create_most_hours_byholiday(df_main)
df_byweekend = create_most_hours_byweekend(df_main)
df_byworkingday = create_most_hours_byworkingday(df_main)

# Baris pertama
st.title("Bike Sharing Dashboard")
st.subheader("Jumlah Penyewaan Sepeda per Bulan")
fig = plt.figure(figsize=[12, 6])
sns.set_style("whitegrid")
ax = sns.lineplot(
    data=df_bike_rental,
    x=df_bike_rental["mnth"],
    y=df_bike_rental["cnt"],
    hue=df_bike_rental["yr"],
    marker="o",
    palette=["#00008B", "#008000"],
    legend="full",
    linewidth=2,
)
ax.xaxis.set_major_locator(ticker.MultipleLocator(1))
plt.xlabel("Bulan ke-", size=12)
plt.ylabel("Jumlah Penyewaan Sepeda (kali)", size=12)
plt.legend(title="Tahun", loc="upper left", bbox_to_anchor=(1, 1))
st.pyplot(fig)

# Baris kedua
st.subheader("Musim dengan Jumlah Pelanggan Paling Banyak")
fig, ax = plt.subplots(nrows=1, ncols=2, figsize=[24, 8])
colors = ["#00008B", "#D3D3D3", "#D3D3D3", "#D3D3D3"]
sns.barplot(
    data=df_bycasual,
    x=df_bycasual["casual"],
    y=df_bycasual["season"],
    palette=colors,
    ax=ax[0],
)
ax[0].set_title(
    "Berdasarkan Jumlah Pelanggan yang Belum Mendaftar", loc="center", size=22
)
ax[0].set_xlabel(None)
ax[0].set_ylabel(None)
ax[0].tick_params(axis="x", labelsize=17)
ax[0].tick_params(axis="y", labelsize=20)
sns.barplot(
    data=df_byregistered,
    x=df_byregistered["registered"],
    y=df_byregistered["season"],
    palette=colors,
    ax=ax[1],
)
ax[1].set_title(
    "Berdasarkan Jumlah Pelanggan yang Telah Mendaftar", loc="center", size=22
)
ax[1].set_xlabel(None)
ax[1].set_ylabel(None)
ax[1].tick_params(axis="x", labelsize=17)
ax[1].tick_params(axis="y", labelsize=20)
ax[1].invert_xaxis()
ax[1].yaxis.set_label_position("right")
ax[1].yaxis.tick_right()
st.pyplot(fig)

# Baris ketiga
st.subheader("Jam-Jam dengan Jumlah Penyewaan Sepeda Paling Banyak")
fig_1, ax_1 = plt.subplots(nrows=1, ncols=3, figsize=[30, 8])
colors = ["#00008B"]
sns.barplot(
    data=df_byholiday,
    x=df_byholiday["hr"],
    y=df_byholiday["cnt"],
    palette=colors,
    ax=ax_1[0],
)
ax_1[0].set_title("Saat Holiday", loc="center", size=22)
ax_1[0].set_xlabel("Penunjuk Jam di Angka", fontsize=20)
ax_1[0].set_ylabel(None)
ax_1[0].tick_params(axis="x", labelsize=18)
ax_1[0].tick_params(axis="y", labelsize=17)
sns.barplot(
    data=df_byweekend,
    x=df_byweekend["hr"],
    y=df_byweekend["cnt"],
    palette=colors,
    ax=ax_1[1],
)
ax_1[1].set_title("Saat Weekend", loc="center", size=22)
ax_1[1].set_xlabel("Penunjuk Jam di Angka", fontsize=20)
ax_1[1].set_ylabel(None)
ax_1[1].tick_params(axis="x", labelsize=18)
ax_1[1].tick_params(axis="y", labelsize=17)
sns.barplot(
    data=df_byworkingday,
    x=df_byworkingday["hr"],
    y=df_byworkingday["cnt"],
    palette=colors,
    ax=ax_1[2],
)
ax_1[2].set_title("Saat Workingday", loc="center", size=22)
ax_1[2].set_xlabel("Penunjuk Jam di Angka", fontsize=20)
ax_1[2].set_ylabel(None)
ax_1[2].tick_params(axis="x", labelsize=18)
ax_1[2].tick_params(axis="y", labelsize=17)
st.pyplot(fig_1)
