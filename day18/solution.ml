(* Advent of Code 2021, jour 18.
   Un nombre est un arbre binaire immuable. Pour l'explosion, explode_aux
   descend en mémorisant le chemin depuis la racine (liste de Left/Right
   contenant les sous-arbres frères) ; rebuild remonte ce chemin en
   ajoutant les deux valeurs à la feuille la plus à droite du premier frère
   gauche et à la plus à gauche du premier frère droit (idée du zipper).
   explode et split renvoient None quand la règle ne s'applique pas, ce qui
   permet à reduce de respecter l'ordre de priorité des règles. *)

type tree = Leaf of int | Node of tree * tree

let is_digit c = match c with '0' .. '9' -> true | _ -> false

let read_number s i =
  let j = ref i in
  let n = ref 0 in
  while !j < String.length s && is_digit s.[!j] do
    n := (10 * !n) + (int_of_char s.[!j] - int_of_char '0');
    incr j
  done;
  (Leaf !n, !j)

(* arbre lu à partir de s.[i] et indice qui suit *)
let rec parse_tree s i =
  if is_digit s.[i] then read_number s i
  else
    let left, i1 = parse_tree s (i + 1) in
    let right, i2 = parse_tree s (i1 + 1) in
    (Node (left, right), i2 + 1)

let lire_nombres nom =
  let ic = open_in nom in
  let rec lire () =
    match input_line ic with
    | l -> fst (parse_tree l 0) :: lire ()
    | exception End_of_file -> close_in ic; []
  in
  lire ()

(* Left b : on est descendu à gauche, b est le frère droit ;
   Right a : on est descendu à droite, a est le frère gauche. *)
type path = Left of tree | Right of tree

let rec add_rightmost t v =
  match t with
  | Leaf n -> Leaf (n + v)
  | Node (a, b) -> Node (a, add_rightmost b v)

let rec add_leftmost t v =
  match t with
  | Leaf n -> Leaf (n + v)
  | Node (a, b) -> Node (add_leftmost a v, b)

(* Reconstruit l'arbre en remontant le chemin ; chaque valeur à ajouter
   l'est une seule fois, au premier frère rencontré du bon côté. *)
let rec rebuild path t left_add right_add =
  match path, left_add, right_add with
  | [], _, _ -> t
  | Right tl :: q, Some v, _ -> rebuild q (Node (add_rightmost tl v, t)) None right_add
  | Right tl :: q, None, _ -> rebuild q (Node (tl, t)) None right_add
  | Left tr :: q, _, Some v -> rebuild q (Node (t, add_leftmost tr v)) left_add None
  | Left tr :: q, _, None -> rebuild q (Node (t, tr)) left_add None

let rec explode_aux t path depth =
  match t with
  | Leaf _ -> None
  | Node (Leaf a, Leaf b) when depth >= 4 ->
    Some (rebuild path (Leaf 0) (Some a) (Some b))
  | Node (a, b) -> (
      match explode_aux a (Left b :: path) (depth + 1) with
      | None -> explode_aux b (Right a :: path) (depth + 1)
      | Some t -> Some t)

let explode t = explode_aux t [] 0

let rec split t =
  match t with
  | Leaf n when n > 9 -> Some (Node (Leaf (n / 2), Leaf ((n + 1) / 2)))
  | Leaf _ -> None
  | Node (a, b) -> (
      match split a with
      | Some a' -> Some (Node (a', b))
      | None -> (
          match split b with
          | None -> None
          | Some b' -> Some (Node (a, b'))))

let rec reduce t =
  match explode t with
  | Some t' -> reduce t'
  | None -> ( match split t with Some t' -> reduce t' | None -> t)

let rec magnitude t =
  match t with
  | Leaf n -> n
  | Node (a, b) -> (3 * magnitude a) + (2 * magnitude b)

let partie1 snails =
  let addition =
    List.fold_left (fun t1 t2 -> reduce (Node (t1, t2))) (List.hd snails) (List.tl snails)
  in
  magnitude addition

(* Remarque : filter ((<>) x) écarte tous les nombres égaux à x, et pas
   seulement x lui-même ; c'est sans effet si l'entrée n'a pas de doublon. *)
let partie2 snails =
  List.fold_left max 0
    (List.map
       (fun x ->
          List.fold_left max 0
            (List.map (fun y -> magnitude (reduce (Node (x, y))))
               (List.filter (( <> ) x) snails)))
       snails)

let () =
  let snails = lire_nombres "input.txt" in
  Printf.printf "Partie 1 : %d\n" (partie1 snails);
  Printf.printf "Partie 2 : %d\n" (partie2 snails)
