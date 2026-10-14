(* Advent of Code 2021, jour 1.
   Version récursive avec accumulateur : la partie 1 garde la valeur
   précédente, la partie 2 garde les trois dernières valeurs pour mettre à
   jour la somme de la fenêtre glissante. *)

let lire_profondeurs nom =
  let ic = open_in nom in
  let rec lire () =
    match input_line ic with
    | ligne -> int_of_string (String.trim ligne) :: lire ()
    | exception End_of_file -> close_in ic; []
  in
  lire ()

(* Nombre d'éléments plus grands que leur prédécesseur. *)
let partie1 profondeurs =
  let rec compter l precedent acc =
    match l with
    | [] -> acc
    | t :: q -> compter q t (if t > precedent then acc + 1 else acc)
  in
  match profondeurs with
  | [] -> failwith "liste vide"
  | t :: q -> compter q t 0

(* La fenêtre courante vaut w = w1 + w2 + w3 ; la suivante s'obtient en
   retirant w1 et en ajoutant le nouvel élément. *)
let partie2 profondeurs =
  let rec compter l w w1 w2 w3 acc =
    match l with
    | [] -> acc
    | t :: q ->
      let nw = w - w1 + t in
      compter q nw w2 w3 t (if nw > w then acc + 1 else acc)
  in
  match profondeurs with
  | w1 :: w2 :: w3 :: q -> compter q (w1 + w2 + w3) w1 w2 w3 0
  | _ -> failwith "moins de trois mesures"

let () =
  let profondeurs = lire_profondeurs "input.txt" in
  Printf.printf "Partie 1 : %d\n" (partie1 profondeurs);
  Printf.printf "Partie 2 : %d\n" (partie2 profondeurs)
