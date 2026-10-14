(* Advent of Code 2021, jour 2.
   Les commandes sont converties en un type somme ; une fonction de
   transition par partie (apply1, apply2) met à jour l'état, et on la
   replie sur la liste des commandes. *)

type direction = Forward | Up | Down

let direction_of_string s =
  match s with
  | "forward" -> Forward
  | "up" -> Up
  | "down" -> Down
  | _ -> failwith "direction inconnue"

let lire_commandes nom =
  let ic = Scanf.Scanning.open_in nom in
  let rec lire () =
    match Scanf.bscanf ic " %s %d" (fun d a -> (direction_of_string d, a)) with
    | commande -> commande :: lire ()
    | exception _ -> Scanf.Scanning.close_in ic; []
  in
  lire ()

let apply1 (pos, depth) (dir, amount) =
  match dir with
  | Forward -> (pos + amount, depth)
  | Up -> (pos, depth - amount)
  | Down -> (pos, depth + amount)

(* Dans la partie 2, up et down modifient la visée (aim). *)
let apply2 (pos, depth, aim) (dir, amount) =
  match dir with
  | Forward -> (pos + amount, depth + aim * amount, aim)
  | Up -> (pos, depth, aim - amount)
  | Down -> (pos, depth, aim + amount)

let partie1 commandes =
  let pos, depth = List.fold_left apply1 (0, 0) commandes in
  pos * depth

let partie2 commandes =
  let pos, depth, _ = List.fold_left apply2 (0, 0, 0) commandes in
  pos * depth

let () =
  let commandes = lire_commandes "input.txt" in
  Printf.printf "Partie 1 : %d\n" (partie1 commandes);
  Printf.printf "Partie 2 : %d\n" (partie2 commandes)
