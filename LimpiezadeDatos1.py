import pandas as pd
import matplotlib.pyplot as plt
import os

datos = pd.read_csv(r"C:\Users\LENOVO\Documents\Python\LimpiezadeDatos.csv",encoding='latin-1')
data = pd.DataFrame(datos)
'''
Comenzamos la Limpieza de datos con la funcion, en donde aplicamos dos tipos de formato a la columna
Fecha de factura que contiene el dataframe original, para poder separar la fecha y la hora en cada columa
'''
def Converir_fecha(fecha_str):
    try:
        return pd.to_datetime(fecha_str, format= '%m/%d/%Y %H:%M:%S')
    except:
        try:
            return pd.to_datetime(fecha_str, format='%m/%d/%Y %H:%M')
        except:
            return pd.NaT

'''
Continuamos con la limpieza de datos, como quitar las letras A y C de la columna Num Factura,
quitar numeros negativos y pasarlos a positivos de las columnas Monto y Cantidad asi como cambiar las comas(,) por puntos decimales(.)
Crear las columnas fecha y hora por separado 
'''
data['Fecha Nueva'] = data['Fecha de factura'].apply(Converir_fecha)
data['Pais'] = data['Pais'].astype('string')
data['Cantidad'] = data['Cantidad'].abs()
data['Monto'] = data['Monto'].astype(str).str.replace(',','.').astype(float)
data['Monto'] = data['Monto'].abs()
data['ID Cliente'] = data['ID Cliente'].fillna(0)
data['Num Factura'] = data['Num Factura'].astype(str).str.replace('C','', regex=False)
data['Num Factura'] = data['Num Factura'].str.replace('A','',regex=False)
data = data.drop_duplicates()


NuevoData = pd.DataFrame({'Num Factura': data['Num Factura'].astype(int),
                          'Fecha': data['Fecha Nueva'].dt.normalize(),
                          'Hora': data['Fecha Nueva'].dt.time,
                          'ID Cliente': data['ID Cliente'],
                          'Pais': data['Pais'],
                          'Cantidad': data['Cantidad'],
                          'Monto': data['Monto']})


NuevoData = NuevoData.drop_duplicates()
VentasMen = NuevoData.resample('ME', on='Fecha')['Cantidad'].sum()
VentasMen = pd.DataFrame(VentasMen)

print(NuevoData['Fecha'].head())

'''
plt.figure(figsize=(10,5))
plt.plot(VentasMen.index, VentasMen['Cantidad'])
plt.title('Ventas Mensuales')
plt.xlabel('Fechas por Mes')
plt.ylabel('Ventas')
plt.grid(True)
plt.show()
'''
'''
NuevoData.to_excel('Ventas por Factura.xlsx', sheet_name='Ventas', index = False)
'''