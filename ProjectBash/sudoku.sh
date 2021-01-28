#!/bin/bash

array_with_element_from_file=()
array_to_play=()

create_array() {
    for col in {0..8}
    do
        for row in {0..8}
        do
            # index=$[($col*9)+$row]
            array_to_play+=(0)
            array_with_element_from_file+=(0)
        done
    done
}

create_array_by_file() {
    # input="array_for_sudoku.txt"
    input="solution.txt"
    while IFS= read -r line
    do
        for element in $line
        do
            element="${element/$'\r'/}"
            array_to_play+=($element)
            array_with_element_from_file+=($element)
        done
    done < "$input"
}

get_index(){
    echo "     0 1 2    3 4 5    6 7 8\n"
}

print_row_border() {
    border="  "
    for count in {0..27}; do
        border="$border="
    done
    border="$border \n"
    echo $border
}

display_array() {
    RED='\033[0;31m'
    GREEN='\033[0;32m'
    YELLOW='\033[1;35m'
    NC='\033[0m'
    display_array_tab=$(get_index)
    display_array_tab="${RED}$display_array_tab${NC}$(print_row_border)"
    for col in {0..8}
    do
        display_array_tab="$display_array_tab${RED}$col${NC}"
        for row in {0..8}
        do
            index=$[($col*9)+$row]
            if (( $row % 3 == 0 ))
            then
                display_array_tab="$display_array_tab || "
            else
                display_array_tab="$display_array_tab "
            fi
            if ((${array_with_element_from_file[$index]} != 0))
            then
                display_array_tab="$display_array_tab${GREEN}${array_to_play[$index]}${NC}"
            else
                if ((${array_to_play[$index]} != 0))
                then
                    display_array_tab="$display_array_tab${YELLOW}${array_to_play[$index]}${NC}"
                else
                    display_array_tab="$display_array_tab${array_to_play[$index]}"
                fi
            fi
        done
        display_array_tab="$display_array_tab\n"
        
        if (( $col % 3 == 2 ))
        then
            display_array_tab="$display_array_tab$(print_row_border)"
        fi
    done
    
    printf "$display_array_tab"
    
}

check_row_or_col(){
    array_of_numbers=(0 0 0 0 0 0 0 0 0 0)
    for counter in {0..8}
    do
        if (($1 == 0))
        then
            index=$[($2*9)+$counter]
        else
            index=$[($counter*9)+$2]
        fi
        element_to_check_from_array=${array_to_play[$index]}
        if ((${array_of_numbers[$element_to_check_from_array]} == 0))
        then
            array_of_numbers[$element_to_check_from_array]=1
        else
            if (($element_to_check_from_array != 0))
            then
                echo "Error"
            fi
        fi
        
    done
}

check_square(){
    array_of_numbers=(0 0 0 0 0 0 0 0 0 0)
    for row in {0..2}
    do
        for col in {0..2}
        do
            index=$[(($row+3*$2)*9)+($col+3*$1)]
            element_to_check_from_array=${array_to_play[$index]}
            if ((${array_of_numbers[$element_to_check_from_array]} == 0))
            then
                array_of_numbers[$element_to_check_from_array]=1
            else
                if (($element_to_check_from_array != 0))
                then
                    echo "Error"
                fi
            fi
        done
    done
}

check() {
    error=""
    move_col=-1
    move_row=0
    for counter in {0..8}
    do
        error="$error$(check_row_or_col 0 ${counter})"
        error="$error$(check_row_or_col 1 ${counter})"
        move_row=$(( $counter % 3 ))
        if (( $counter % 3 == 0 ))
        then
            move_col=$[$move_col+1]
        fi
        error="$error$(check_square $move_row $move_col)"
        
    done
    echo $error
}

add_element(){
    index=$[($2*9)+$3]
    if ((${array_with_element_from_file[$index]} == 0))
    then
        array_to_play[$index]=$1
    fi
}
check_win() {
    counter_of_zero=0
    for col in {0..8}
    do
        for row in {0..8}
        do
            index=$[($col*9)+$row]
            if ((${array_to_play[$index]} == 0))
            then
                counter_of_zero=$counter_of_zero+1
            fi
        done
    done
    if (($counter_of_zero == 0)) && [ -z $(check) ]
    then
        echo "win"
    else
        echo ""
    fi
    echo ""
}

create_array_by_file
display_array

value=0
message=""
while [ $value -gt -1 ] && [ -z "$(check_win)" ]
do
    clear
    message=$(check)
    echo $message
    if [ -z "$message" ] || (($value == 0))
    then
        echo ""
    else
        echo "Masz Błąd "
    fi
    display_array
    echo "value col row"
    read value col row
    if [ -z "$value" ] || [ -z "$col" ] || [ -z "$row" ]
    then
        echo "\$var is empty"
        value=0
    else
        add_element $value $row $col
    fi
    
done
clear
display_array
echo "Wygrałeś"