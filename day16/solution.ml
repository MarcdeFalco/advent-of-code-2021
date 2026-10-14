(* Advent of Code 2021, jour 16.
   Descente récursive : trois fonctions mutuellement récursives lisent un
   paquet ou une liste de sous-paquets (par longueur ou par nombre) et
   renvoient l'arbre lu avec le nombre de bits consommés. Le flux est lu
   bit à bit grâce à un enregistrement mutable (caractère, bit courant).
   Partie 1 : somme des versions ; partie 2 : valeur de l'expression. *)

type bitstream = {
  s : string;
  mutable pos : int; (* caractère hexadécimal courant *)
  mutable sub_pos : int (* bit courant dans ce caractère, de 0 à 3 *)
}

let get_bit b =
  let c =
    match b.s.[b.pos] with
    | '0' .. '9' as c -> int_of_char c - int_of_char '0'
    | 'A' .. 'F' as c -> 10 + int_of_char c - int_of_char 'A'
    | _ -> failwith "caractère invalide"
  in
  let bit = (c lsr (3 - b.sub_pos)) mod 2 in
  if b.sub_pos = 3 then begin
    b.pos <- b.pos + 1;
    b.sub_pos <- 0
  end
  else b.sub_pos <- b.sub_pos + 1;
  bit

(* entier codé par les n bits suivants *)
let get_number b n =
  let rec aux n acc = if n = 0 then acc else aux (n - 1) (2 * acc + get_bit b) in
  aux n 0

type operator = Plus | Mult | Max | Min | Gt | Lt | Eq

(* Litteral (valeur, version) | Operator (opérateur, sous-paquets, version) *)
type packet =
  | Litteral of int * int
  | Operator of operator * packet list * int

(* l'identifiant 4 désigne un littéral : la case correspondante ne sert pas *)
let operator_of_pid pid = [| Plus; Mult; Min; Max; Plus; Gt; Lt; Eq |].(pid)

(* valeur d'un littéral et nombre de bits lus *)
let get_litteral_value b =
  let rec aux acc count =
    let header = get_bit b in
    let value = get_number b 4 in
    let nacc = 16 * acc + value in
    if header = 0 then (nacc, count * 5) else aux nacc (count + 1)
  in
  aux 0 1

let rec get_packet b =
  let version = get_number b 3 in
  let pid = get_number b 3 in
  if pid = 4 then begin
    let lit, lit_size = get_litteral_value b in
    (Litteral (lit, version), lit_size + 6)
  end
  else begin
    let lid = get_bit b in
    let sub, size =
      if lid = 0 then
        let length = get_number b 15 in
        let sl = get_sub_packets_length b length in
        (sl, length + 15 + 7)
      else
        let count = get_number b 11 in
        let sl, size = get_sub_packets_count b count in
        (sl, size + 11 + 7)
    in
    (Operator (operator_of_pid pid, sub, version), size)
  end

(* sous-paquets occupant exactement l bits *)
and get_sub_packets_length b l =
  if l = 0 then []
  else
    let p, size = get_packet b in
    p :: get_sub_packets_length b (l - size)

(* n sous-paquets, avec le nombre total de bits lus *)
and get_sub_packets_count b n =
  if n = 0 then ([], 0)
  else
    let p, size = get_packet b in
    let pl, sizel = get_sub_packets_count b (n - 1) in
    (p :: pl, size + sizel)

let rec version packet =
  match packet with
  | Litteral (_, v) -> v
  | Operator (_, sub, v) -> v + List.fold_left ( + ) 0 (List.map version sub)

let rec fold op l =
  match l with
  | [] -> failwith "aucun argument"
  | [ x ] -> x
  | hd :: tl -> op hd (fold op tl)

let cmp_gt x y = if x > y then 1 else 0
let cmp_lt x y = if x < y then 1 else 0
let cmp_eq x y = if x = y then 1 else 0

let rec value packet =
  match packet with
  | Litteral (lit, _) -> lit
  | Operator (op, sub, _) ->
    let sub_values = List.map value sub in
    fold
      (match op with
       | Plus -> ( + )
       | Mult -> ( * )
       | Max -> max
       | Min -> min
       | Gt -> cmp_gt
       | Lt -> cmp_lt
       | Eq -> cmp_eq)
      sub_values

let partie1 p = version p
let partie2 p = value p

let () =
  let ic = open_in "input.txt" in
  let s = String.trim (input_line ic) in
  close_in ic;
  let p, _ = get_packet { s; pos = 0; sub_pos = 0 } in
  Printf.printf "Partie 1 : %d\n" (partie1 p);
  Printf.printf "Partie 2 : %d\n" (partie2 p)
