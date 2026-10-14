(* Advent of Code 2021, jour 4.
   Les cases rayées deviennent Struck. À chaque tirage, on raye le numéro
   sur toutes les grilles en jeu, puis on retire de la liste les grilles
   gagnantes, que l'on accumule : la première gagnante donne la partie 1,
   la dernière la partie 2. *)

type tile = Number of string | Struck

let read_board ic =
  let _ = input_line ic in (* ligne vide *)
  Array.init 5 (fun _ ->
      input_line ic
      |> String.split_on_char ' '
      |> List.filter (( <> ) "")
      |> List.map (fun s -> Number s)
      |> Array.of_list)

let lire_entree nom =
  let ic = open_in nom in
  let numbers = String.split_on_char ',' (input_line ic) in
  let rec read_boards acc =
    match read_board ic with
    | b -> read_boards (b :: acc)
    | exception End_of_file -> close_in ic; acc
  in
  (numbers, read_boards [])

let won b =
  let flag = ref false in
  for i = 0 to 4 do
    let bcol = ref true in
    let brow = ref true in
    for j = 0 to 4 do
      bcol := !bcol && b.(j).(i) = Struck;
      brow := !brow && b.(i).(j) = Struck
    done;
    flag := !flag || !bcol || !brow
  done;
  !flag

let strike n b =
  for i = 0 to 4 do
    for j = 0 to 4 do
      if b.(i).(j) = Number n then b.(i).(j) <- Struck
    done
  done

(* winners : couples (numéro gagnant, grille), le plus récent en tête. *)
let rec play boards numbers winners =
  match numbers, boards with
  | _, [] | [], _ -> winners
  | n :: q, _ ->
    List.iter (strike n) boards;
    let new_winners = List.map (fun b -> (n, b)) (List.filter won boards) in
    let new_boards = List.filter (fun b -> not (won b)) boards in
    play new_boards q (new_winners @ winners)

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

let partie1 winners = score (List.hd (List.rev winners))
let partie2 winners = score (List.hd winners)

let () =
  let numbers, boards = lire_entree "input.txt" in
  let winners = play boards numbers [] in
  Printf.printf "Partie 1 : %d\n" (partie1 winners);
  Printf.printf "Partie 2 : %d\n" (partie2 winners)
