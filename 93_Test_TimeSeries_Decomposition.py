import pandas as pd
import statsmodels.api as sm
import matplotlib.pyplot as plt  # !!!!!


decomp_freq = int(24 * 60 / 15 * 7)

centrum_galerie = pd.read_csv('Centrum-Galerie-Belegung.csv',
                              names=['Datum', 'Belegung'],
                              index_col=['Datum'],
                              parse_dates=True)
print(centrum_galerie)
centrum_galerie.Belegung.plot()


res = sm.tsa.seasonal_decompose(centrum_galerie.Belegung.interpolate(),
                                freq=decomp_freq,
                                model='additive')
res_plot = res.plot()
plt.show()  # !!!!!
