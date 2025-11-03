# ![NextGen Travels Logo](./next_gen_travel.jpg) NextGen Travels – Exploratory Data Analysis de Destinos Turísticos

## 🌎 Acerca de NextGen Travels

En **NextGen Travels** nos apasiona transformar los datos en experiencias únicas. Sabemos que elegir un destino turístico no es solo cuestión de playas o monumentos, sino de una combinación de factores que hacen que la experiencia sea **segura, cómoda y memorable**.

Nuestro servicio combina **opiniones de turistas** con **índices objetivos** sobre economía, gastronomía, seguridad, infraestructura, nivel de inglés, transporte, alojamiento y más. Gracias a esto, ofrecemos **recomendaciones personalizadas de destinos** que se adaptan a las prioridades de cada viajero, ayudándolos a tomar decisiones informadas y a maximizar su satisfacción.

Fundada en **2025** por el visionario **Alvaro Martinez**, NextGen Travels nació con la misión de **modernizar el sector turístico mediante análisis de datos innovadores**. Desde entonces, la empresa se ha convertido en un **referente internacional**, guiando a millones de viajeros a experiencias inolvidables y ayudando a los países turísticos a **mejorar sus índices de calidad, seguridad y servicio**, potenciando así su atractivo global.

Con un enfoque que combina **innovación tecnológica** y **pasión por los viajes**, NextGen Travels no solo asesora a los viajeros, sino que también colabora con destinos turísticos para **optimizar su infraestructura, gastronomía, seguridad y servicios**, garantizando que cada viaje sea una experiencia excepcional.

---

## 📊 Datos Analizados

El análisis abarca **17 países** de América, Asia y Oceanía:

- **América:** Argentina, Brasil, Chile, Bolivia, Colombia, México, Perú  
- **Oceanía:** Australia, Nueva Zelanda  
- **Asia:** China, Laos, Indonesia, Filipinas, Tailandia, Vietnam, Malasia, Camboya  

Y utiliza **más de 45 variables** que cubren áreas como:

### Opinión de turistas
- `Nota Global`  
- `Acogida`  
- `Comunicacion`  
- `Cultura`  
- `Gastronomia`  
- `Hoteles`  
- `Paisajes`  
- `Limpieza`  
- `Seguridad`  
- `Tranquilidad`  
- `Transportes`  
- `Ciudades`
- `Presupuesto`   

### Economía
- `PIB (U.S. dollars)`  
- `Ahorro nacional bruto (% de PIB)`  
- `% Inflacion anual`  
- `Poblacion (Millones)`  
- `Inversion (% de PIB)`  
- `% paro`  

### Gastronomía
- `top 50 restaurantes`  
- `Nota gastronomica`  
- `Ranking mundial`  
- `Platos en top 100`  

### Seguridad y Criminalidad
- `Indice de Criminalidad`  
- `Indice de Seguridad`  
- `Ranking Corrupcion`  
- `Indice de Corrupcion`  

### Amabilidad y Facilidad de Adaptación
- `Ranking amabilidad locales`  
- `Ranking facilidad de adaptación al país`  
- `Ranking bienvenida calurosa`  
- `Ranking facilidad de tener amigos locales`  
- `Ranking facilidad para hacer amigos`  

### Turismo y Alojamiento
- `Numero de turistas`  
- `Numero de camas`  
- `Numero de hoteles`  
- `Numero de habitaciones`  
- `Ratio de ocupacion`  
- `Numero de personas en sector turismo`  
- `% poblacion que trabaja en turismo`  

### Nivel de Inglés
- `Total English speakers`  
- `% personas que hablan ingles`  

### Transporte y Seguridad Vial
- `Total Km carreteras`  
- `muertes en carretera por cada 100.000 habitantes`  
- `muertes en carretera por cada 100.000 vehiculos`  
- `Total fallecidos al año`  

---

## 🎯 Objetivo del Análisis

El análisis permite a NextGen Travels:

1. **Comparar destinos** usando tanto **datos objetivos** como **percepciones de turistas**.  
2. **Identificar fortalezas y debilidades** de cada país en áreas clave: seguridad, gastronomía, infraestructura, transporte, alojamiento y amabilidad local.  
3. **Recomendar destinos personalizados** según las prioridades del viajero, ya sea economía, tranquilidad, gastronomía, cultura o aventura.  
4. **Visualizar tendencias turísticas** y anticipar experiencias futuras para los clientes.  

---

## 🔍 Metodología

1. **Recolección y limpieza de datos**: combinamos información de encuestas de turistas, estadísticas oficiales y rankings de organismos internacionales.

Las fuentes de información son las siguientes y han sido obtenidas mediante **APIs**, descargas de **xlsx/csv/json** y **web scraping**:

1. [Banco Mundial – Llegadas internacionales](https://datos.bancomundial.org/indicador/ST.INT.ARVL?end=2020&start=2020&year=2020)  
2. [World Population Review – Países más amigables](https://worldpopulationreview.com/country-rankings/friendliest-countries)  
3. [Datos Mundial – Corrupción](https://www.datosmundial.com/corrupcion.php?full)  
4. [Numbeo – Clasificación por criminalidad](https://es.numbeo.com/criminalidad/clasificaciones-por-pa%C3%ADs)  
5. [Fondo Monetario Internacional – World Economic Outlook](https://www.imf.org/en/Publications/SPROLLs/world-economic-outlook-databases)  
6. [TasteAtlas – Mejores cocinas](https://www.tasteatlas.com/best/cuisines)  
7. [TasteAtlas – Mejores platos](https://www.tasteatlas.com/best/dishes)  
8. [Kaggle – World's Best Restaurants](https://www.kaggle.com/datasets/thomasfranois/worlds-best-restaurants)  
9. [UNTourism – Estadísticas de turismo](https://www.untourism.int/tourism-statistics)  
10. [Wikipedia – Población que habla inglés](https://en.wikipedia.org/wiki/List_of_countries_by_English-speaking_population)  
11. [Tour du Mondiste – Mejores países Asia Sudeste](https://www.tourdumondiste.com/plus-beaux-pays-asie-du-sud-est)  
12. [Tour du Mondiste – Opiniones Argentina](https://www.tourdumondiste.com/avis-conseils-bons-plans-argentine)  
13. [Tour du Mondiste – Opiniones Brasil](https://www.tourdumondiste.com/avis-conseils-bons-plans-bresil)  
14. [Tour du Mondiste – Opiniones Chile](https://www.tourdumondiste.com/avis-voyage-chili)  
15. [Tour du Mondiste – Opiniones Bolivia](https://www.tourdumondiste.com/avis-conseils-bons-plans-bolivie)  
16. [Tour du Mondiste – Opiniones Colombia](https://www.tourdumondiste.com/avis-conseils-bons-plans-colombie)  
17. [Tour du Mondiste – Opiniones México](https://www.tourdumondiste.com/avis-conseils-bons-plans-mexique)  
18. [Tour du Mondiste – Opiniones Perú](https://www.tourdumondiste.com/avis-conseils-bons-plans-perou)  
19. [Tour du Mondiste – Opiniones Australia](https://www.tourdumondiste.com/avis-conseils-bons-plans-australie)  
20. [Tour du Mondiste – Opiniones Nueva Zelanda](https://www.tourdumondiste.com/avis-voyage-nouvelle-zelande)  
21. [Tour du Mondiste – Opiniones China](https://www.tourdumondiste.com/avis-voyage-chine)  
22. [Wikipedia – Tasa de muertes por accidentes de tránsito](https://es.wikipedia.org/wiki/Anexo:Pa%C3%ADses_por_tasa_de_muertes_por_siniestros_de_tr%C3%A1nsito)  
23. [IndexMundi – Mapa de indicadores](https://www.indexmundi.com/map/?v=115&l=es)
24. [Numbeo – Clasificación por indice de costes de vida](https://es.numbeo.com/coste-de-vida/clasificaciones-por-pa%C3%ADs)



2. **Exploratory Data Analysis (EDA)**: análisis descriptivo, correlaciones, rankings y comparaciones entre países.  
3. **Visualizaciones interactivas**: gráficos de radar, heatmaps, y dashboards comparativos.  
4. **Modelo de recomendación**: permite ponderar variables según las preferencias del cliente y generar un ranking personalizado de destinos.

---

## 💡 Beneficios para el Cliente

- **Elección de destino basada en datos reales** y experiencias de otros turistas.  
- **Información detallada de seguridad y confort**, incluyendo transporte, nivel de inglés y sanidad.  
- **Recomendaciones personalizadas** según presupuesto, interés en gastronomía, naturaleza, cultura o relax.  
- **Comparativa objetiva de destinos** en un solo vistazo, evitando sorpresas durante el viaje.  

---

## 📈 Próximos Pasos

- Integración con **Dashboard interactivo** para que el cliente pueda ajustar prioridades en tiempo real.  
- Incorporación de **reviews recientes** de turistas y nuevas métricas de sostenibilidad y ecoturismo.  
- Desarrollo de **sistema de scoring personalizado** que combine datos objetivos y subjetivos para cada viajero.  

---

**NextGen Travels** transforma datos complejos en decisiones de viaje inteligentes y experiencias inolvidables. 🌏✈️  

![NextGen Travels Logo](./next_gen_travel.jpg)