import pandas as pd
df = pd.read_csv(r"C:\Users\franc\OneDrive\Escritorio\python\dolar.csv")
for col in ["Comprador", "Vendedor"]:
    df[col] = df[col].str.replace(".", "", regex=False)   # saca separador de miles
    df[col] = df[col].str.replace(",", ".", regex=False)  # coma -> punto decimal
    df[col] = df[col].astype(float)
df["Fecha"] = pd.to_datetime(df["Fecha"], format="%d-%m-%Y")
df = df.sort_values("Fecha")
print(df.head())
print(df.dtypes)
import matplotlib.pyplot as plt

plt.figure(figsize=(12, 6))
plt.plot(df["Fecha"], df["Vendedor"], label="Dólar vendedor", color="steelblue")
plt.plot(df["Fecha"], df["Comprador"], label="Dólar comprador", color="lightblue")
plt.title("Evolución del dólar minorista (CABA) 2010-2026")
plt.xlabel("Fecha")
plt.ylabel("Pesos por dólar")
plt.legend()
plt.grid(alpha=0.3)
plt.tight_layout()
plt.savefig("dolar_evolucion.png")
plt.show()

inflacion = pd.read_csv(r"C:\Users\franc\OneDrive\Escritorio\python\inflacion.csv", sep="\t")

inflacion["Fecha"] = pd.to_datetime(inflacion["Fecha"], format="%d/%m/%Y")
inflacion["Valor"] = inflacion["Valor"].astype(str).str.replace(",", ".").astype(float)

inflacion = inflacion.sort_values("Fecha")

inflacion["Indice"] = 100 * (1 + inflacion["Valor"] / 100).cumprod()

print(inflacion.head())
print(inflacion.tail())

dolar_mensual = df.set_index("Fecha").resample("ME")["Vendedor"].last().reset_index()

inflacion_m = inflacion.set_index("Fecha").resample("ME")["Indice"].last().reset_index()

datos = pd.merge_asof(dolar_mensual.sort_values("Fecha"), 
                        inflacion_m.sort_values("Fecha"), 
                        on="Fecha")

indice_base = datos["Indice"].iloc[0]
dolar_base = datos["Vendedor"].iloc[0]

datos["Dolar_Real"] = dolar_base * (datos["Indice"] / indice_base)

print(datos.head())
print(datos.tail())

plt.figure(figsize=(12, 6))
plt.plot(datos["Fecha"], datos["Vendedor"], label="Dólar nominal", color="steelblue")
plt.plot(datos["Fecha"], datos["Dolar_Real"], label="Dólar si solo hubiera seguido la inflación", 
         color="orange", linestyle="--")
plt.title("Dólar nominal vs. dólar ajustado por inflación (2010-2026)")
plt.xlabel("Fecha")
plt.ylabel("Pesos por dólar (escala log)")
plt.legend()
plt.grid(alpha=0.3)
plt.tight_layout()
plt.savefig("dolar_vs_inflacion.png")
plt.show()