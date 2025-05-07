# Copyright © 2025 Maxence Cailleteau - HEIG-VD - GRIPIT
# SPDX‑License‑Identifier: GPL‑3.0-or-later
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License 
# and any later version.
#______________________________________________________________________


import pdfkit   #pip install pdfkit
from pdfkit.api import configuration
import numpy as np
import os

import scenarios.datas as dt
import scenarios.scenarios_masses as scma

def get_info(df):
    
    dTot = df['xCg'][len(df)-1]
    tTot = df['t'][len(df)-1]
    vMax = max(df['vXCg'])
    aMax = max(df['aXCg'])
    aMin = min(df['aXCg'])
    for i in range(len(df['t'])):
        if df['t'][i] <= np.single(1):
            dAccel = df['xCg'][i]
        else:
            break
    dFrein = 0
    tFrein = 0
    dContact = 0
    tContact = 0
    for i in range(len(df['fxFreinAvG'])):
        if df['fxFreinAvG'][i] < np.single(-500):
            dFrein = df['xCg'][i]
            tFrein = df['t'][i]
            break
    for i in range(len(df['entreferAvGz'])):
        if df['entreferAvGz'][i] > (dt.upLev*1000+1E-2):
            dContact = df['xCg'][i]
            tContact = df['t'][i]
            break
    dVol = dFrein-dContact
    tVol = tFrein-tContact
    n = np.single(0)
    dy = np.single(0)
    dz = np.single(0)
    for i in range(len(df['t'])):
        t = df['t'][i]
        if t >= np.single(1) and t <= tFrein:
            n = n + 1
            dy = dy + df['entreferAvGy'][i]
            dz = dz + df['entreferAvGz'][i]
    dy = dy/n
    dz = dz/n
    return dTot, tTot, vMax, aMax, aMin, dAccel, dFrein, dVol, tVol, tFrein, dy, dz

def content(df):
    dTot, tTot, vMax, aMax, aMin, dAccel, dFrein, dVol, tVol, tFrein, dy, dz = get_info(df)

    # Remplacez les chemins d'accès réels des images et les données du tableau ici
    img0_path = dt.img0_path   #str(dt.figuresPath + "Resultats_integration_dans_le_temps.png")
    img0_title = "Resultats de l'integration dans le temps"
    img0_descriptor = f"""
    xCg, yCg, zCg : positions en X, Y et Z du centre de gravité;<br>
    vXCg, vYCg, vZCg : vitesses en X, Y et Z du centre de gravité;<br>
    aXCg, aYCg, aZCg : accélérations en X, Y et Z du centre de gravité;<br>
    tangage, vTangage, aTangage : position, vitesse et accélération de rotation du véhicule selon l'axe Oy;<br>
    lacet, vLacet, aLacet : position, vitesse et accélération de rotation du véhicule selon l'axe Oz;<br>
    roulis, vRoulis, aRoulis : position, vitesse et accélération de rotation du véhicule selon l'axe Ox;
    """

    img1_path = dt.img1_path   #str(dt.figuresPath + "Resultats_integration_selon_la_distance.png")
    img1_title = "Resultats de l'integration selon la position en X du centre de gravité"
    img1_descriptor = f"""
    xCg, yCg, zCg : positions en X, Y et Z du centre de gravité;<br>
    vXCg, vYCg, vZCg : vitesses en X, Y et Z du centre de gravité;<br>
    aXCg, aYCg, aZCg : accélérations en X, Y et Z du centre de gravité;<br>
    tangage, vTangage, aTangage : position, vitesse et accélération de rotation du véhicule selon l'axe Oy;<br>
    lacet, vLacet, aLacet : position, vitesse et accélération de rotation du véhicule selon l'axe Oz;<br>
    roulis, vRoulis, aRoulis : position, vitesse et accélération de rotation du véhicule selon l'axe Ox;
    """

    img2_path = dt.img2_path   #str(dt.figuresPath + "Entrefers_Z_selon_le_temps.png")
    img2_title = "Entrefer vertical"
    img2_descriptor = f"""Entrefer vertical (Z) des modules selon le temps."""

    img3_path = dt.img3_path   #str(dt.figuresPath + "Entrefers_Y_selon_le_temps.png")
    img3_title = "Entrefer latéral"
    img3_descriptor = f"""Entrefer vertical (Y) des modules selon le temps."""

    img4_path = dt.img4_path   #str(dt.figuresPath + "Positions_2D_-_s.png")
    img4_title = "Positions des éléments"
    img4_descriptor = f"""Positions 2D des éléments sur le rail selon le temps."""

    img5_path = dt.img5_path   #str(dt.figuresPath + "Forces_X_selon_le_temps_[N].png")
    img5_title = "Forces en X des modules"
    img5_descriptor = f"""Forces appliquées aux modules dans le sens de la marche (X)."""

    img6_path = dt.img6_path   #str(dt.figuresPath + "Forces_Y_selon_le_temps_[N].png")
    img6_title = "Forces en Y des modules"
    img6_descriptor = f"""Forces appliquées aux modules latéralement (Y)."""

    img7_path = dt.img7_path   #str(dt.figuresPath + "Forces_Z_selon_le_temps_[N].png")
    img7_title = "Forces en Z des modules"
    img7_descriptor = f"""Forces appliquées aux modules verticalement (Z)."""

    img8_path = dt.img8_path   #str(dt.figuresPath + "Integration modules_Y_-_s.png")
    img8_title = "Mouvement en Y des modules"
    img8_descriptor = f"""Résultats de l'intégration des modules latéralement (Y)."""

    img9_path = dt.img9_path   #str(dt.figuresPath + "Integration_modules_Z_-_s.png")
    img9_title = "Mouvement en Z des modules"
    img9_descriptor = f"""Résultats de l'intégration des modules verticalement (Z)."""

    img10_path = dt.img10_path   #str(dt.figuresPath + "Deformation_ressort_Y.png")
    img10_title = "Longueur des amortisseurs latéraux"
    img10_descriptor = f"""Longueur des amortisseurs latéraux (Y)"""

    img11_path = dt.img11_path   #str(dt.figuresPath + "Deformation_ressort_Z.png")
    img11_title = "Longueur des amortisseurs verticaux"
    img11_descriptor = f"""Longueur des amortisseurs verticaux (Z)"""

    img12_path = dt.img12_path   #str(dt.figuresPath + 'Magnetic forces for ideal air gap = %.1fmm - magnets : %s'%(dt.idealYairGag*1000, dt.magnetDim) + ".png")
    img12_title = 'Magnetic forces for ideal air gap = %.1fmm - magnets : %s'%(dt.idealYairGag*1000, dt.magnetDim)
    img12_descriptor = f"""Forces électromagnetiques pour un entre-fer donné."""

    img13_path = dt.img13_path
    img13_title = "Entrefer vertical selon la distance"
    img13_descriptor = f"""Entrefer vertical (Z) des modules selon la position en X du centre de gravité."""

    img14_path = dt.img14_path 
    img14_title = "Entrefer latéral selon la distance"
    img14_descriptor = f"""Entrefer vertical (Y) des modules selon la position en X du centre de gravité."""

    img15_path = dt.img15_path 
    img15_title = "Vitesse deformation_ressort_Y"
    img15_descriptor = f"""Vitesse en fonction du temps."""

    img16_path = dt.img16_path 
    img16_title = "Vitesse deformation_ressort_Z"
    img16_descriptor = f"""Vitesse en fonction du temps."""

    img17_path = dt.img17_path 
    img17_title = "Force fct. déformation ressorts Y"
    img17_descriptor = f"""Force en fonction de la déformation."""

    img18_path = dt.img18_path 
    img18_title = "Force fct. déformation ressorts Z"
    img18_descriptor = f"""Force en fonction de la déformation."""

    img19_path = dt.img19_path 
    img19_title = "Déformation ressorts Y"
    img19_descriptor = f"""Déformation en fonction du temps."""

    img20_path = dt.img20_path 
    img20_title = "Déformation ressorts Z"
    img20_descriptor = f"""Déformation en fonction du temps."""

    img21_path = dt.img21_path 
    img21_title = "Force fct. vitesse déformation ressorts Y"
    img21_descriptor = f"""Force en fonction de la vitesse de déformation."""

    img22_path = dt.img22_path 
    img22_title = "Force fct. vitesse déformation ressorts Z"
    img22_descriptor = f"""Force en fonction de la vitesse de déformation."""

    img23_path = dt.img23_path
    img23_title = "Force ressorts Y fct temps [csv]"
    img23_descriptor = f"""Force en fonction du temps."""

    img24_path = dt.img24_path
    img24_title = "Force ressorts Z fct temps [csv]"
    img24_descriptor = f"""Force en fonction du temps."""

    #fProp, durée accél, fFrein, distance max, kz, ky, ksi z, ksi y, entrefer de départ
    table_parameters = f"""
    <tr>
        <td>Entrefer vetical (z) initial</td>
        <td>{"%.1f"%(dt.upLev*1000)}</td>
        <td>mm</td>
    </tr>
    <tr>
        <td>Longueur de rail amagnetique</td>
        <td>{"%.1f"%(dt.cancelFMagnMeters)}</td>
        <td>m</td>
    </tr>
    <tr>
        <td>Pression supposée Pohwaro</td>
        <td>{"%.1f"%(dt.pression)}</td>
        <td>bar</td>
    </tr>
    <tr>
        <td>Force de propulsion</td>
        <td>{"%d"%(dt.bstForce)}</td>
        <td>N</td>
    </tr>
    <tr>
        <td>Durée accélération</td>
        <td>{"%.3f"%(dt.bstDureeDecharge)}</td>
        <td>s</td>
    </tr>
    <tr>
        <td>Force de freinage (x4)</td>
        <td>{"%d (%d)"%(dt.fBrake*dt.coefFriction*dt.perfFrein, dt.fBrake*dt.coefFriction*dt.perfFrein*4)}</td>
        <td>N/frein (N)</td>
    </tr>
    <tr>
        <td>Coef. friction dyn. plaquette</td>
        <td>{"%.1f"%(dt.coefFriction)}</td>
        <td>-</td>
    </tr>
    <tr>
        <td>Course max (CG)</td>
        <td>{"%d"%(dt.posXCgStop)}</td>
        <td>m</td>
    </tr>
    <tr>
        <td>Raideur verticale : kz</td>
        <td>{"%d"%(dt.kZ)}</td>
        <td>N/m</td>
    </tr>
    <tr>
        <td>Raideur latérale : ky</td>
        <td>{"%d"%(dt.kY)}</td>
        <td>N/m</td>
    </tr>
    <tr>
        <td>Taux d'amortissement verticale : ksi z</td>
        <td>{"%.3f"%(dt.ksiZ)}</td>
        <td>-</td>
    </tr>
    <tr>
        <td>Taux d'amortissement latéral : ksi y</td>
        <td>{"%.3f"%(dt.ksiY)}</td>
        <td>-</td>
    </tr>
    <tr>
        <td>Coef. frottement fluide verticale : c z</td>
        <td>{"%.3f"%(dt.cZ)}</td>
        <td>N.s/m</td>
    </tr>
    <tr>
        <td>Coef. frottement fluide latéral : c y</td>
        <td>{"%.3f"%(dt.cY)}</td>
        <td>N.s/m</td>
    </tr>
    <!-- Ajoutez d'autres lignes au besoin -->
    """

    #mTot, mCoque, mChassis, mProp, mEau, mModule, mChargement
    table_masses = f"""
    <tr>
        <td>Coque</td>
        <td>{"%d"%(dt.podGeom[1][3])}</td>
        <td>kg</td>
    </tr>
    <tr>
        <td>Châssis</td>
        <td>{"%d"%(dt.podGeom[0][3])}</td>
        <td>kg</td>
    </tr>
    <tr>
        <td>Booster</td>
        <td>{"%d"%(dt.bstMasseVide)}</td>
        <td>kg</td>
    </tr>
    <tr>
        <td>Eau</td>
        <td>{"%d"%(dt.bstMasseEau)}</td>
        <td>kg</td>
    </tr>
    <tr>
        <td>Module (x4)</td>
        <td>{"%d (%d)"%(dt.masseModule, dt.masseModule*4)}</td>
        <td>kg</td>
    </tr>
    <tr>
        <td>Chargement</td>
        <td>{"%d"%(dt.podGeom[2][3])}</td>
        <td>kg</td>
    </tr>
    <tr>
        <td>Total</td>
        <td>{"%d"%(dt.masseTot)}</td>
        <td>kg</td>
    </tr>
    <tr>
        <td>A vide (sans eau)</td>
        <td>{"%d"%(dt.masseTot - dt.bstMasseEau)}</td>
        <td>kg</td>
    </tr>
    """

    # dTot, tTot, vMax, aMax, aMin, dAccel, dFrein, dVol, tVol
    table_results = f"""
    <tr>
        <td>Distance parcourue</td>
        <td>{"%.1f%s (%d)"%((dTot/dt.posXCgStop)*100, "%", dTot)}</td>
        <td>% (m)</td>
    </tr>
    <tr>
        <td>Distance d'acceleration'</td>
        <td>{"%d"%(dAccel)}</td>
        <td>m</td>
    </tr>
    <tr>
        <td>Distance de vol</td>
        <td>{"%d"%(dVol)}</td>
        <td>m</td>
    </tr>
    <tr>
        <td>Distance de freinage</td>
        <td>{"%.1f"%(dTot-dFrein)}</td>
        <td>m</td>
    </tr>
    <tr>
        <td>Durée totale</td>
        <td>{"%.1f"%(tTot)}</td>
        <td>s</td>
    </tr>
    <tr>
        <td>Durée de vol</td>
        <td>{"%.1f"%(tVol)}</td>
        <td>s</td>
    </tr>
    <tr>
        <td>Durée de freinage</td>
        <td>{"%.1f"%(tTot-tFrein)}</td>
        <td>s</td>
    </tr>
    <tr>
        <td>Vitesse max</td>
        <td>{"%.2f  (%d)"%(vMax, vMax*3.6)}</td>
        <td>m/s (km/h)</td>
    </tr>
    <tr>
        <td>Accélération max</td>
        <td>{"%.2f  (%.1f)"%(aMax, aMax/9.81)}</td>
        <td>m/s2 (g)</td>
    </tr>
    <tr>
        <td>Décélération max</td>
        <td>{"%.2f  (%.1f)"%(aMin, aMin/9.81)}</td>
        <td>m/s2 (g)</td>
    </tr>
    <tr>
        <td>Entrefer latéral moyen en vol</td>
        <td>{"%.1f"%(dy)}</td>
        <td>mm</td>
    </tr>
    <tr>
        <td>Entrefer vertical moyen en vol</td>
        <td>{"%.1f"%(dz)}</td>
        <td>mm</td>
    </tr>
    
    
    """

    #----------------------------------------------------------------------------
    html_content = f"""
    <!DOCTYPE html>
    <html lang="fr">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Rapport Technique</title>
        <style>
            body {{
                margin: 0;
                padding: 0;
                font-family: Arial, sans-serif;
                display: flex;
            }}

            .colonne1 {{
                background-color: #023047; /* Couleur de la première colonne */
                width: 5%;
            }}

            .colonne2 {{
                flex: 1; /* La deuxième colonne prend le reste de l'espace disponible */
                padding: 20px; /* Ajoutez un espace de remplissage au besoin */
                border: 1px solid #ccc; /* Bordure autour de la deuxième colonne */
                position: relative; /* Position relative pour aligner les éléments à droite */
            }}

            h1 {{
                color: #fb8500;
            }}

            h2 {{
                color: #ffb703;
            }}

            h3 {{
                color: #219ebc;
            }}

            table {{
                width: 50%;
                margin: 0 auto;
                border-collapse: collapse;
                margin-bottom: 20px;
            }}

            table, th, td {{
                border: 1px solid black;
            }}

            th, td {{
                padding: 10px;
                text-align: center;
            }}

            section {{
                border-top: 1px solid #ccc; /* Ligne de séparation entre chaque section */
                margin-top: 20px; /* Marge au-dessus de la ligne de séparation */
                padding-top: 20px; /* Espace de remplissage au-dessus de la ligne de séparation */
            }}

            .info-droite {{
                position: absolute;
                top: 20px; /* Ajustez la position verticale au besoin */
                right: 20px; /* Ajustez la position horizontale au besoin */
                text-align: right;
            }}

            .colonne2 img {{
                width: 100%; /* Redimensionner l'image pour occuper 100% de la largeur de la colonne 2 */
                border: 1px solid #ccc;
                margin-bottom: 10px; /* Ajoutez une marge en bas de l'image */
            }}
        </style>
    </head>
    <body>

        <div class="colonne1"></div>

        <div class="colonne2">
            <h1>Compte rendu de simulation</h1>
            <p></p>
            <p></p>
            <p></p>
            <p><b>Notes :</b> {dt.note_pdf}</p>
            <p>Scénario de masses : {scma.masse_version}</p>
            <p>Scénario de aimants : {dt.magnetDim}</p>
            <p>Multiplicateur des forces électromagnétiques (X) : {"%d %s"%(dt.multMagX*100, "%")}</p>
            <p>Multiplicateur des forces électromagnétiques (Y) : {"%d %s"%(dt.multMagY*100, "%")}</p>
            <p>Multiplicateur des forces électromagnétiques (Z) : {"%d %s"%(dt.multMagZ*100, "%")}</p>
            <p>{dt.outputFileName}</p>

            <section>
                <h2>Paramètres</h2>

                <!-- Tableau -->
                <table>
                    <tr>
                        <th>Description</th>
                        <th>Valeur</th>
                        <th>Unité</th>
                    </tr>
                    <tr>
                        {table_parameters}
                    </tr>
                    <!-- Ajoutez d'autres lignes au besoin -->
                </table>
            </section>

            <section>
                <h2>Bilan de masses</h2>

                <!-- Tableau -->
                <table>
                    <tr>
                        <th>Description</th>
                        <th>Valeur</th>
                        <th>Unité</th>
                    </tr>
                    <tr>
                        {table_masses}
                    </tr>
                    <!-- Ajoutez d'autres lignes au besoin -->
                </table>
            </section>

            <div style="page-break-before: always;"></div>

            <section>
                <h2>Résultats</h2>
                <!-- Tableau -->
                <table>
                    <tr>
                        <th>Description</th>
                        <th>Valeur</th>
                        <th>Unité</th>
                    </tr>
                    <tr>
                        {table_results}
                    </tr>
                    <!-- Ajoutez d'autres lignes au besoin -->
                </table>
            </section>

            <section>
                <h3>{img0_title}</h3>
                <img src={img0_path} alt={img0_title}>
                <p>{img0_descriptor}</p>
            </section>

            <div style="page-break-before: always;"></div>

            <section>
                <h3>{img1_title}</h3>
                <img src={img1_path} alt={img1_title}>
                <p>{img1_descriptor}</p>
            </section>

            <section>
                <h3>{img2_title}</h3>
                <img src={img2_path} alt={img2_title}>
                <p>{img2_descriptor}</p>
            </section>

            <div style="page-break-before: always;"></div>
            
            <section>
                <h3>{img3_title}</h3>
                <img src={img3_path} alt={img3_title}>
                <p>{img3_descriptor}</p>
            </section>

            <section>
                <h3>{img4_title}</h3>
                <img src={img4_path} alt={img4_title}>
                <p>{img4_descriptor}</p>
            </section>

            <div style="page-break-before: always;"></div>
            
            <section>
                <h3>{img5_title}</h3>
                <img src={img5_path} alt={img5_title}>
                <p>{img5_descriptor}</p>
            </section>

            <section>
                <h3>{img6_title}</h3>
                <img src={img6_path} alt={img6_title}>
                <p>{img6_descriptor}</p>
            </section>

            <div style="page-break-before: always;"></div>
            
            <section>
                <h3>{img7_title}</h3>
                <img src={img7_path} alt={img7_title}>
                <p>{img7_descriptor}</p>
            </section>

            <section>
                <h3>{img8_title}</h3>
                <img src={img8_path} alt={img8_title}>
                <p>{img8_descriptor}</p>
            </section>

            <div style="page-break-before: always;"></div>
            
            <section>
                <h3>{img9_title}</h3>
                <img src={img9_path} alt={img9_title}>
                <p>{img9_descriptor}</p>
            </section>

            <section>
                <h3>{img10_title}</h3>
                <img src={img10_path} alt={img10_title}>
                <p>{img10_descriptor}</p>
            </section>

            <div style="page-break-before: always;"></div>
            
            <section>
                <h3>{img11_title}</h3>
                <img src={img11_path} alt={img11_title}>
                <p>{img11_descriptor}</p>
            </section>

            <section>
                <h3>{img13_title}</h3>
                <img src={img13_path} alt={img13_title}>
                <p>{img13_descriptor}</p>
            </section>

            <div style="page-break-before: always;"></div>
            
            <section>
                <h3>{img14_title}</h3>
                <img src={img14_path} alt={img14_title}>
                <p>{img14_descriptor}</p>
            </section>

            <section>
                <h3>{img12_title}</h3>
                <img src={img12_path} alt={img12_title}>
                <p>{img12_descriptor}</p>
            </section>

            <div style="page-break-before: always;"></div>
            
            <section>
                <h3>{img23_title}</h3>
                <img src={img23_path} alt={img23_title}>
                <p>{img23_descriptor}</p>
            </section>

            <section>
                <h3>{img24_title}</h3>
                <img src={img24_path} alt={img24_title}>
                <p>{img24_descriptor}</p>
            </section>

            <div style="page-break-before: always;"></div>
            
            <section>
                <h3>{img19_title}</h3>
                <img src={img19_path} alt={img19_title}>
                <p>{img19_descriptor}</p>
            </section>

            <section>
                <h3>{img20_title}</h3>
                <img src={img20_path} alt={img20_title}>
                <p>{img20_descriptor}</p>
            </section>

            <div style="page-break-before: always;"></div>
            
            <section>
                <h3>{img15_title}</h3>
                <img src={img15_path} alt={img15_title}>
                <p>{img15_descriptor}</p>
            </section>

            <section>
                <h3>{img16_title}</h3>
                <img src={img16_path} alt={img16_title}>
                <p>{img16_descriptor}</p>
            </section>

            <div style="page-break-before: always;"></div>
            
            <section>
                <h3>{img17_title}</h3>
                <img src={img17_path} alt={img17_title}>
                <p>{img17_descriptor}</p>
            </section>

            <section>
                <h3>{img18_title}</h3>
                <img src={img18_path} alt={img18_title}>
                <p>{img18_descriptor}</p>
            </section>

            <div style="page-break-before: always;"></div>
            
            <section>
                <h3>{img21_title}</h3>
                <img src={img21_path} alt={img21_title}>
                <p>{img21_descriptor}</p>
            </section>

            <section>
                <h3>{img22_title}</h3>
                <img src={img22_path} alt={img22_title}>
                <p>{img22_descriptor}</p>
            </section>

            <!-- Ajoutez d'autres sections ici avec leurs propres titres, images, descriptions, etc. -->

            <!-- Nom et date alignés à droite -->
            <div class="info-droite">
                <p>Le script original de cet outil de simulation a été créé par M.Cailleteau <br> à la HEIG-VD dans le cadre du projet GRIPIT/Ohwaboo en 2024</p>
                <p>Date du jour : 
                    <script>
                        var today = new Date();
                        document.write(today.toLocaleDateString());
                    </script>
                </p>
                <p>{dt.htmlName}</p>
                <p>Généré automatiquement</p>
            </div>

        </div>

    </body>
    </html>
    """
    return html_content

def gen_html(html_content):
    print("Création du html.")
    # Écrivez le contenu généré dans un fichier HTML
    input_html_file = str(dt.outFile + dt.htmlName)
    with open(input_html_file, "w", encoding="utf-8") as file:
        file.write(html_content)

#def makepdf(html_content):
#    """Generate a PDF file from a string of HTML."""
#    htmldoc = HTML(string=html_content, base_url="")
#    return htmldoc.write_pdf()
#
#def gen_pdf(infile, outfile):
#    html = Path(infile).read_text()
#    pdf = makepdf(html)
#    Path(outfile).write_bytes(pdf)

def delete_files(input_html):
    print("Suppresion des fichiers temporaires.")
    os.remove(input_html)
    os.remove(dt.img0_path)
    os.remove(dt.img1_path)
    os.remove(dt.img2_path)
    os.remove(dt.img3_path)
    os.remove(dt.img4_path)
    os.remove(dt.img5_path)
    os.remove(dt.img6_path)
    os.remove(dt.img7_path)
    os.remove(dt.img8_path)
    os.remove(dt.img9_path)
    os.remove(dt.img10_path)
    os.remove(dt.img11_path)
    os.remove(dt.img12_path)
    os.remove(dt.img13_path)
    os.remove(dt.img14_path)

def html_to_pdf(input_html, output_pdf, options=None):
    """
    Convertit un fichier HTML en PDF.

    :param input_html: Chemin vers le fichier HTML d'entrée.
    :param output_pdf: Chemin de sortie du fichier PDF.
    :param options: Options supplémentaires pour wkhtmltopdf (facultatif).
        # Exemple d'utilisation
        input_html_file = 'chemin/vers/votre/fichier.html'
        output_pdf_file = 'chemin/vers/votre/fichier.pdf'
        html_to_pdf(input_html_file, output_pdf_file)
    """
    print("Création du pdf.")
    #dt.img0_path  = str("file:///" + dt.img0_path )
    #dt.img1_path  = str("file:///" + dt.img1_path )
    #dt.img2_path  = str("file:///" + dt.img2_path )
    #dt.img3_path  = str("file:///" + dt.img3_path )
    #dt.img4_path  = str("file:///" + dt.img4_path )
    #dt.img5_path  = str("file:///" + dt.img5_path )
    #dt.img6_path  = str("file:///" + dt.img6_path )
    #dt.img7_path  = str("file:///" + dt.img7_path )
    #dt.img8_path  = str("file:///" + dt.img8_path )
    #dt.img9_path  = str("file:///" + dt.img9_path )
    #dt.img10_path = str("file:///" + dt.img10_path)
    #dt.img11_path = str("file:///" + dt.img11_path)
    #dt.img12_path = str("file:///" + dt.img12_path)
    if options is None:
        options = {'page-size': 'A3', "enable-local-file-access": ""}
    wkhtml_path = pdfkit.configuration(wkhtmltopdf = "C:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe")  #by using configuration you can add path value.
    try:
        pdfkit.from_file(input_html, output_pdf, options=options, configuration = wkhtml_path)
    except:
        pass
    delete_files(input_html)
    print("Fichiers créés et supprimés.")

#_____________________________________________________________________________________________________________________________________________________________________
if __name__ == "__main__":
    input_html_file = "C:/Users/Max/Documents/GRIPIT_Simulations/out/11-28_13-34_Compte_rendu_simu.html"
    output_pdf_file = "C:/Users/Max/Documents/GRIPIT_Simulations/out/11-28_13-34_Compte_rendu_simu.pdf"
    html_to_pdf(input_html_file, output_pdf_file)
    pass
    #gen_html()

    #gen_pdf(str(dt.dir_path+"/out/rapport_technique.html"), str(dt.dir_path+"/out/out.pdf"))


