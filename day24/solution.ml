(* Advent of Code 2021, jour 24.
   Exécution symbolique du programme : chaque registre contient une
   expression des chiffres d'entrée w1..w14 (Var i), simplifiée au fil de
   l'eau par des règles de réécriture et des bornes d'intervalle. Quand une
   comparaison eql ne peut pas être décidée, on suppose l'égalité vraie et
   on l'enregistre comme contrainte : sur ce programme, chacune relie deux
   chiffres sous la forme w_i = w_j + k. On énumère ensuite les nombres
   satisfaisant toutes les contraintes.
   Hypothèse propre à la forme de ces programmes (z doit revenir à 0). *)

type reg = X | Y | Z | W
type operand = R of reg | C of int
type ope = OpAdd | OpMul | OpDiv | OpMod | OpEql

(* Input i : lecture du i-ème chiffre (de 1 à 14) dans w *)
type instr = Input of int | Instr of ope * reg * operand

let ope_of_string ope =
  match ope with
  | "add" -> OpAdd
  | "mul" -> OpMul
  | "div" -> OpDiv
  | "mod" -> OpMod
  | "eql" -> OpEql
  | _ -> failwith "opération invalide"

let reg_of_string r =
  match r with
  | "x" -> X
  | "y" -> Y
  | "z" -> Z
  | "w" -> W
  | _ -> failwith "registre invalide"

let operand_of_string op =
  match op with
  | "x" | "y" | "z" | "w" -> R (reg_of_string op)
  | _ -> C (int_of_string op)

let read_instr ic input =
  let tokens = String.split_on_char ' ' (String.trim (input_line ic)) in
  if List.hd tokens = "inp" then Input input
  else
    match tokens with
    | [ ope; reg1; op ] ->
      Instr (ope_of_string ope, reg_of_string reg1, operand_of_string op)
    | _ -> failwith "instruction invalide"

let rec read_program ic input =
  match read_instr ic input with
  | i ->
    let next_input = match i with Input _ -> input + 1 | _ -> input in
    i :: read_program ic next_input
  | exception End_of_file -> []

type expr =
  | Add of expr * expr
  | Mul of expr * expr
  | Div of expr * expr
  | Mod of expr * expr
  | Eql of expr * expr
  | Var of int
  | Constant of int

type abstract_alu = { x : expr; y : expr; z : expr; w : expr }

let rec depth e =
  match e with
  | Add (e1, e2) | Mul (e1, e2) | Mod (e1, e2) | Div (e1, e2) | Eql (e1, e2) ->
    1 + max (depth e1) (depth e2)
  | _ -> 0

(* Ordre canonique des opérandes d'une opération commutative : la plus
   profonde à gauche, les constantes à droite. *)
let swap e1 e2 =
  if depth e1 < depth e2 then true
  else
    match e1, e2 with
    | Constant 0, Constant v when v <> 0 -> true
    | Constant 1, Constant v when v <> 1 -> true
    | Constant _, Var _ -> true
    | Var _, Constant _ -> false
    | Var _, Var _ -> false
    | Var _, _ -> true
    | _ -> false

(* Encadrement grossier de la valeur d'une expression (chiffres de 1 à 9). *)
let rec bounds e =
  match e with
  | Constant v -> (v, v)
  | Var _ -> (1, 9)
  | Add (e1, e2) ->
    let min1, max1 = bounds e1 in
    let min2, max2 = bounds e2 in
    (min1 + min2, max1 + max2)
  | Eql (_, _) -> (0, 1)
  | Div (e, Constant v) ->
    let mn, mx = bounds e in
    (mn / v, mx / v)
  | Mod (_, Constant v) -> (0, v - 1)
  | _ -> (-100000, 100000)

let rec simpl e =
  match e with
  | Add (e', Constant 0) -> simpl e'
  (* associativité, constantes regroupées à droite *)
  | Add (e1, Add (e2, e3)) -> simpl (Add (Add (e1, e2), e3))
  | Mul (e1, Mul (e2, e3)) -> simpl (Mul (Mul (e1, e2), e3))
  | Add (Add (e', Constant v1), Constant v2) -> simpl (Add (e', Constant (v1 + v2)))
  | Add (Add (e1, Constant v), e2) -> simpl (Add (Add (e1, e2), Constant v))
  | Mul (Mul (e', Constant v1), Constant v2) -> simpl (Mul (e', Constant (v1 * v2)))
  | Div (Div (e', Constant v1), Constant v2) -> simpl (Div (e', Constant (v1 * v2)))
  (* évaluation des constantes *)
  | Add (Constant v1, Constant v2) -> Constant (v1 + v2)
  | Mul (Constant v1, Constant v2) -> Constant (v1 * v2)
  | Div (Constant v1, Constant v2) -> Constant (v1 / v2)
  | Mod (Constant v1, Constant v2) -> Constant (v1 mod v2)
  | Mul (_, Constant 0) -> Constant 0
  | Mul (e', Constant 1) -> simpl e'
  | Div (Mul (e', Constant v), Constant w) when v = w -> simpl e'
  | Mod (Constant 0, _) -> Constant 0
  | Div (e', Constant 1) -> simpl e'
  (* règles utilisant les bornes et la divisibilité *)
  | Div (e', Constant v) when snd (bounds e') < v -> Constant 0
  | Mod (Mul (_, Constant w), Constant v) when w mod v = 0 -> Constant 0
  | Div (Mul (e1, Constant w), Constant v) when w mod v = 0 -> Mul (e1, Constant (w / v))
  (* distributivité (heuristique, suffisante pour ce programme) *)
  | Mod (Add (e1, e2), e') -> simpl (Add (Mod (e1, e'), Mod (e2, e')))
  | Mul (Add (e1, e2), e') -> simpl (Add (Mul (e1, e'), Mul (e2, e')))
  | Div (Add (e1, e2), e') -> simpl (Add (Div (e1, e'), Div (e2, e')))
  | Mod (e', Constant v) ->
    let e' = simpl e' in
    let _, mx = bounds e' in
    if mx < v then e' else Mod (e', Constant v)
  (* comparaisons décidables *)
  | Eql (Var _, Constant n) when n < 1 || n > 9 -> Constant 0
  | Eql (e', Var _) when fst (bounds e') > 9 -> Constant 0
  | Eql (Constant m, Constant n) -> Constant (if m = n then 1 else 0)
  (* forme canonique, puis simplification des sous-expressions *)
  | Add (e1, e2) when swap e1 e2 -> simpl (Add (e2, e1))
  | Mul (e1, e2) when swap e1 e2 -> simpl (Mul (e2, e1))
  | Eql (e1, e2) when swap e1 e2 -> simpl (Eql (e2, e1))
  | Add (e1, e2) ->
    let e'1 = simpl e1 in
    let e'2 = simpl e2 in
    if e'1 <> e1 || e'2 <> e2 then simpl (Add (e'1, e'2)) else e
  | Mul (e1, e2) ->
    let e'1 = simpl e1 in
    let e'2 = simpl e2 in
    if e'1 <> e1 || e'2 <> e2 then simpl (Mul (e'1, e'2)) else e
  | Mod (e1, e2) ->
    let e'1 = simpl e1 in
    let e'2 = simpl e2 in
    if e'1 <> e1 || e'2 <> e2 then simpl (Mod (e'1, e'2)) else e
  | Div (e1, e2) ->
    let e'1 = simpl e1 in
    let e'2 = simpl e2 in
    if e'1 <> e1 || e'2 <> e2 then simpl (Div (e'1, e'2)) else e
  | Eql (e1, e2) ->
    let e'1 = simpl e1 in
    let e'2 = simpl e2 in
    if e'1 <> e1 || e'2 <> e2 then simpl (Eql (e'1, e'2)) else e
  | _ -> e

(* Exécute une instruction ; renvoie le nouvel état et, le cas échéant, la
   contrainte d'égalité supposée vraie. *)
let apply instr alu =
  let set_reg r v =
    let v = simpl v in
    match r with
    | X -> { alu with x = v }
    | Y -> { alu with y = v }
    | Z -> { alu with z = v }
    | W -> { alu with w = v }
  in
  let get_reg r = match r with X -> alu.x | Y -> alu.y | Z -> alu.z | W -> alu.w in
  let get_ope ope = match ope with R r -> get_reg r | C v -> Constant v in
  match instr with
  | Input i -> ({ alu with w = Var i }, None)
  | Instr (OpAdd, r1, ope) -> (set_reg r1 (Add (get_reg r1, get_ope ope)), None)
  | Instr (OpMul, r1, ope) -> (set_reg r1 (Mul (get_reg r1, get_ope ope)), None)
  | Instr (OpDiv, r1, ope) -> (set_reg r1 (Div (get_reg r1, get_ope ope)), None)
  | Instr (OpMod, r1, ope) -> (set_reg r1 (Mod (get_reg r1, get_ope ope)), None)
  | Instr (OpEql, r1, ope) -> (
      let e' = simpl (Eql (get_reg r1, get_ope ope)) in
      match e' with
      (* égalité indécidable : on la suppose vraie *)
      | Eql (e1, e2) -> (set_reg r1 (Constant 1), Some (e1, e2))
      | _ -> (set_reg r1 e', None))

let rec get_var e =
  match e with
  | Add (e1, e2) | Mul (e1, e2) | Mod (e1, e2) | Div (e1, e2) | Eql (e1, e2) ->
    get_var e1 @ get_var e2
  | Var i -> [ i ]
  | _ -> []

(* valeur de e quand son unique variable vaut v *)
let rec reduce e v =
  match e with
  | Add (e1, e2) -> reduce e1 v + reduce e2 v
  | Mul (e1, e2) -> reduce e1 v * reduce e2 v
  | Div (e1, e2) -> reduce e1 v / reduce e2 v
  | Mod (e1, e2) -> reduce e1 v mod reduce e2 v
  | Eql (e1, e2) -> if reduce e1 v = reduce e2 v then 1 else 0
  | Constant c -> c
  | Var _ -> v

(* d * 10^p *)
let rec digit d p = if p = 0 then d else 10 * digit d (p - 1)

(* Contrainte e(w_j) = w_i : liste des contributions w_j * 10^(14-j) +
   w_i * 10^(14-i) pour tous les couples de chiffres possibles. *)
let unify pair =
  match pair with
  | e, Var i -> (
      match get_var e with
      | [ j ] ->
        List.concat
          (List.init 9 (fun v ->
               let r = reduce e (v + 1) in
               if 0 < r && r < 10 then [ digit (v + 1) (14 - j) + digit r (14 - i) ]
               else []))
      | _ -> failwith "contrainte invalide")
  | _ -> failwith "contrainte invalide"

(* toutes les sommes obtenues en choisissant une contribution par liste *)
let rec expand l =
  match l with
  | sl :: l' ->
    let el' = expand l' in
    List.concat_map (fun n -> List.map (( + ) n) el') sl
  | [] -> [ 0 ]

let nombres_valides program =
  let alu = { x = Constant 0; y = Constant 0; z = Constant 0; w = Constant 0 } in
  let rec eval p alu =
    match p with
    | i :: p' -> (
        let alu', contrainte = apply i alu in
        let contraintes = eval p' alu' in
        match contrainte with None -> contraintes | Some pair -> pair :: contraintes)
    | [] -> []
  in
  List.sort compare (expand (List.map unify (eval program alu)))

let partie1 nombres = List.hd (List.rev nombres) (* le plus grand *)
let partie2 nombres = List.hd nombres (* le plus petit *)

let () =
  let ic = open_in "input.txt" in
  let program = read_program ic 1 in
  close_in ic;
  let nombres = nombres_valides program in
  Printf.printf "Partie 1 : %d\n" (partie1 nombres);
  Printf.printf "Partie 2 : %d\n" (partie2 nombres)
