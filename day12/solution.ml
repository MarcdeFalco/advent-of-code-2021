(* Advent of Code 2021, jour 12.
   Les sommets (des noms) sont numérotés pour construire les listes
   d'adjacence. Retour sur trace : visit additionne les chemins obtenus en
   prolongeant par chaque voisin autorisé ; l'ensemble persistant smalls
   contient les petites cavernes visitées et double indique si la seconde
   visite permise (partie 2) est déjà utilisée. *)

let lire_aretes nom =
  let ic = open_in nom in
  let rec lire () =
    match input_line ic |> String.split_on_char '-' with
    | [ v1; v2 ] -> (v1, v2) :: lire ()
    | _ -> lire ()
    | exception End_of_file -> close_in ic; []
  in
  lire ()

let assocs = lire_aretes "input.txt"

let vertices =
  let l1, l2 = List.split assocs in
  Array.of_list (List.sort_uniq compare (l1 @ l2))

exception Found of int

let array_index v x =
  try
    for i = 0 to Array.length v - 1 do
      if v.(i) = x then raise (Found i)
    done;
    raise Not_found
  with Found i -> i

module IntSet = Set.Make (Int)

(* graph.(i) : liste des voisins du sommet i *)
let graph =
  Array.init (Array.length vertices) (fun i ->
      List.map (array_index vertices)
        (List.map fst (List.filter (fun c -> snd c = vertices.(i)) assocs)
         @ List.map snd (List.filter (fun c -> fst c = vertices.(i)) assocs)))

let is_small v = String.lowercase_ascii v = v

let rec visit x smalls double =
  List.fold_left ( + ) 0
    (List.map
       (fun i ->
          let v = vertices.(i) in
          match v with
          | "start" -> 0
          | "end" -> 1
          | _ when is_small v ->
            if IntSet.mem i smalls then
              (if double then 0 else visit i smalls true)
            else visit i (IntSet.add i smalls) double
          | _ -> visit i smalls double)
       graph.(x))

let partie1 () = visit (array_index vertices "start") IntSet.empty true
let partie2 () = visit (array_index vertices "start") IntSet.empty false

let () =
  Printf.printf "Partie 1 : %d\n" (partie1 ());
  Printf.printf "Partie 2 : %d\n" (partie2 ())
