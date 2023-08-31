# TP-Synthese-Capture-De-Mesures-Raspberry-Pico-MicroPython
Logiciel qui permet de capturer et de stocker dans une base de données l'angle pointé ou la distance capturée par le capteur de distance.
Projet fait avec un Rapsberry Pico dans le cadre du cours Objets Connectés (420 4B5 MO).

Ce projet permet à l'aide d'un joystick controller un capteur de distance monté sur un servomoteur afin de le faire tourner de gauche à droite.
Un click de joystick permet d'avoir un apperçu de la mesure (angle ou distance) avant de la prendre à l'aide de l'interface Tkinter.

Cette interface communique directement avec le Pico et ses composants.

Une fois la mesure prise, elle est stockée dans une base de données SQLite.
