#!/bin/bash

PLANSZA=("0" "0" "0" "0" "0" "0" "0" "0" "0")

function sprawdzWierszKolumnePrzekatna {
    echo $1 $2 $3 $4
    if [[ ${PLANSZA[$2]} == $1 && ${PLANSZA[$3]} == $1 && ${PLANSZA[$4]} == $1 ]];
    then
        reset
        echo "Wygrywa gracza" $1
        exit
    fi
}

function sprawdzPlansze {
    sprawdzWierszKolumnePrzekatna $1 0 1 2
    sprawdzWierszKolumnePrzekatna $1 3 4 5
    sprawdzWierszKolumnePrzekatna $1 6 7 8
    sprawdzWierszKolumnePrzekatna $1 1 3 6
    sprawdzWierszKolumnePrzekatna $1 1 4 7
    sprawdzWierszKolumnePrzekatna $1 2 5 8
    sprawdzWierszKolumnePrzekatna $1 0 4 8
    sprawdzWierszKolumnePrzekatna $1 2 4 6
    echo "sprawdzPlansze"
}
function pokazPlansze {
    echo ${PLANSZA[0]} "|" ${PLANSZA[1]} "|" ${PLANSZA[2]}
    echo ${PLANSZA[3]} "|" ${PLANSZA[4]} "|" ${PLANSZA[5]}
    echo ${PLANSZA[6]} "|" ${PLANSZA[7]} "|" ${PLANSZA[8]}
}

function wyborGracza {
    echo "Player" $1
    read wybor
    PLANSZA[$wybor]=$1
}

reset
while true
do
 
    pokazPlansze
    wyborGracza 1
    sprawdzPlansze 1
    reset

    pokazPlansze
    wyborGracza 2
    sprawdzPlansze 2
    reset

done

