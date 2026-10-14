(* Advent of Code 2021, jour 3.
   Partie 1 : on compte les '1' de chaque colonne ; le mot des bits
   majoritaires donne m, celui des minoritaires 2^12 - 1 - m.
   Partie 2 : filtrage récursif bit par bit ; le critère minoritaire
   s'obtient en échangeant les deux listes. Largeur 12 écrite en dur. *)

let largeur = 12

let lire_valeurs nom =
  let ic = open_in nom in
  let rec lire () =
    match input_line ic with
    | l -> l :: lire ()
    | exception End_of_file -> close_in ic; []
  in
  lire ()

(* Nombre de mots de l dont le caractère i vaut x. *)
let compte l i x =
  List.fold_left (fun acc s -> if s.[i] = x then acc + 1 else acc) 0 l

let bin2int l = List.fold_left (fun acc b -> 2 * acc + b) 0 l

let partie1 valeurs =
  let n = List.length valeurs in
  let rec majoritaires i =
    if i = largeur then []
    else
      let n1 = compte valeurs i '1' in
      (if n1 >= n / 2 then 1 else 0) :: majoritaires (i + 1)
  in
  let m = bin2int (majoritaires 0) in
  let l = (1 lsl largeur) - m - 1 in
  m * l

let string_to_binlist s =
  List.init (String.length s) (fun i -> if s.[i] = '1' then 1 else 0)

(* Partage de l selon le prédicat f. *)
let rec split l f =
  match l with
  | [] -> ([], [])
  | t :: q ->
    let l1, l2 = split q f in
    if f t then (t :: l1, l2) else (l1, t :: l2)

let rec search l i most =
  match l with
  | [x] -> bin2int (string_to_binlist x)
  | _ ->
    let v1, v0 = split l (fun s -> s.[i] = '1') in
    let n1, n0 = List.length v1, List.length v0 in
    let v1, v0 = if most then (v1, v0) else (v0, v1) in
    if n1 >= n0 then search v1 (i + 1) most else search v0 (i + 1) most

let partie2 valeurs =
  let oxygen = search valeurs 0 true in
  let co2 = search valeurs 0 false in
  oxygen * co2

let () =
  let valeurs = lire_valeurs "input.txt" in
  Printf.printf "Partie 1 : %d\n" (partie1 valeurs);
  Printf.printf "Partie 2 : %d\n" (partie2 valeurs)
