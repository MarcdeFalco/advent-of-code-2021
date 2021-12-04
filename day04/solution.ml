let ic = open_in "input.txt"

let numbers = String.split_on_char ',' (input_line ic)

type tile = Number of string | Struck

let read_board () =
    let _ = input_line ic in
    let b = Array.make 5 [||] in
    for i = 0 to 4 do
        b.(i) <- Array.of_list
            (List.map (fun s -> Number s)
                (List.filter ((<>)"")
                    (String.split_on_char ' ' (input_line ic))))
    done;
    b

let rec read_boards acc =
    try
        let b = read_board () in
        read_boards (b :: acc)
    with End_of_file -> acc

let boards = read_boards []

let won b =
    let flag = ref false in
    for i = 0 to 4 do
        let bcol = ref true in
        let brow = ref true in
        for j = 0 to 4 do
            bcol := !bcol && b.(j).(i) = Struck;
            brow := !brow && b.(i).(j) = Struck;
        done;
        flag := !flag || !bcol || !brow
    done;
    !flag

let strike n b =
    for i = 0 to 4 do
        for j = 0 to 4 do
            if b.(i).(j) = Number n
            then b.(i).(j) <- Struck
        done
    done

let rec play boards numbers winners =
    match numbers, boards with
    | _ , []
    | [], _ -> winners
    | n::q, _ -> 
        List.iter (strike n) boards;
        let new_winners = List.map (fun b -> (n, b) )
              (List.filter won boards) in
        let new_boards = List.filter (fun b -> not (won b)) boards in
        play new_boards q (new_winners @ winners)

let winners = play boards numbers []

let first_winner = List.hd (List.rev winners)
let last_winner = List.hd winners

let score (n, b) =
    let s = ref 0 in
    for i = 0 to 4 do
        for j = 0 to 4 do
            match b.(i).(j) with
            | Number k -> s := !s + int_of_string k
            | Struck -> ()
        done
    done;
    !s * int_of_string n

let _ = 
    Printf.printf "Part 1 %d\n" (score first_winner);
    Printf.printf "Part 2 %d\n" (score last_winner)
