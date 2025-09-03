# Actividad 1: Introducción a DevOps y DevSecOps  
**Nombre:** Ariana Camila Lopez Julcarima
**Fecha:** 03/09/2025  
**Tiempo invertido:** 04:00  

**Entorno utilizado:**  
Laptop personal con navegador Chrome y sistema operativo Windows 11.

---

## 4.1 DevOps vs. Cascada tradicional
El desarrollo de software ha cambiado mucho con el tiempo. Antes se usaban métodos muy estructurados como el modelo en cascada, donde todo se hacía en un orden fijo. El modelo en cascada sigue un flujo lineal de fases donde primero se realiza el análisis, luego el diseño, más adelante la construcción, después las pruebas y finalmente el despliegue. En este esquema el feedback llega tarde y en grandes lotes, lo que implica más riesgo porque los defectos suelen descubrirse solo al final del ciclo, como se describe en The Phoenix Project 2013.

DevOps surge como alternativa moderna y busca integrar desarrollo y operaciones en ciclos continuos con entregas pequeñas y automatizadas. Esto permite validar más rápido y corregir antes de que los problemas crezcan. El reporte Google State of DevOps 2023 muestra que los equipos con prácticas DevOps reducen de manera significativa tanto el tiempo de entrega como la tasa de fallos en producción.
![DevOps vs Cascada](imagenes/devops-vs-cascada.png)

**Pregunta Retadora**
Un contexto donde el modelo en cascada todavía puede ser razonable es el desarrollo de software para militares. En este tipo de proyectos se requieren certificaciones muy estrictas que obliga a llevar un proceso documentado y validaciones completas antes de publicar una versión. Además, gran parte del software está ligado a hardware especializado y un error puede terminar en fallas de seguridad muy costosas o irreparables.

En este escenario se pierde velocidad y flexibilidad en los cambios, pero se gana en confiabilidad y estabilidad. Aunque no se aprovecha toda la agilidad que ofrece DevOps, lo más importante es cumplir con las normas y garantizar que el sistema funcione de manera segura desde el primer despliegue.

## 4.2 Ciclo de dos pasos y silos
En un ciclo de dos pasos donde primero está el desarrollo y luego la operatividad, sin integración continua, aparecen varias limitaciones. Una de ellas es que los cambios se acumulan en grandes lotes, lo que provoca que los errores se descubran tarde y sea más difícil identificar su causa. Otra limitación es la generación de colas de defectos, ya que los equipos encuentran problemas pero no los corrigen de inmediato, lo que retrasa la entrega y eleva el costo de integración. Este esquema refuerza el trabajo en silos, porque cada área se concentra en su parte y el handoff entre equipos se vuelve lento y con poca comunicación, lo que genera un desbalance de información entre ambas áreas.
![Silos organizacionales](imagenes/silos-equipos.png)


**Pregunta Retadora**
Un anti-patrón común es el throw over the wall, que ocurre cuando el equipo de desarrollo termina su trabajo y lo entrega a operaciones como si solo se tratara de pasar la pelota al otro lado del muro. Esto provoca que los de operaciones reciban el software sin suficiente contexto y con poca docoumentación, lo que hace más difícil resolver problemas y aumenta el tiempo medio de recuperación cuando ocurre un incidente.

Otro anti-patrón es ver la seguridad solo como una auditoría tardía, aplicando controles al final del proyecto en lugar de integrarlos desde el inicio. Esto genera retrabajos porque muchas veces se descubren vulnerabilidades cuando ya el sistema está casi terminado y corregir en ese punto cuesta más esfuerzo y tiempo. Además, pueden repetirse las mismas fallas en versiones futuras porque la seguridad nunca se incluyó como parte del proceso diario.

---

## 4.3 Principios y beneficios de DevOps
La integración continua (CI) busca que los cambios de código sean pequeños y frecuentes, lo que permite detectarlos y probarlos de inmediato. Esto se complementa con pruebas automatizadas que se ejecutan cerca del código, reduciendo errores antes de llegar a producción. La entrega continua (CD) se centra en que las mejoras pasen automáticamente desde la fase de integración hasta los entornos de prueba y producción, asegurando despliegues frecuentes. Esto requiere una colaboración constante entre desarrollo y operaciones para que el software llegue a los usuarios sin interrupciones y con menor riesgo.

**Relación con Agile:**  
Una práctica Agile que influye directamente en el pipeline son las reuniones diarias. En estas reuniones cada miembro comparte qué hizo, qué planea hacer y qué obstáculos encontró. Esa información permite que el equipo decida con mayor claridad qué cambios están listos para promover en el pipeline y cuáles conviene bloquear o revisar antes. De la misma forma, en las retrospectivas se analizan incidentes pasados y se definen mejoras que luego se incorporan como reglas en el proceso de integración y despliegue.

Un indicador observable puede ser el tiempo que pasa desde que un Pull Request es aprobado o mergeado hasta que el cambio se despliega en el entorno de pruebas. Este dato refleja la agilidad del equipo y no depende de información financiera. Se puede obtener fácilmente revisando los metadatos del repositorio, que muestran la fecha de aprobación o de merge del PR, y comparándolos con los registros de despliegue guardados en las bitácoras. De esa forma se consigue una medida simple y verificable del nivel de integración entre desarrollo y operaciones.

---