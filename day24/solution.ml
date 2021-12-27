type reg = X | Y | Z | W
type operand = R of reg | C of int
type ope = OpAdd | OpMul | OpDiv | OpMod | OpEql
type instr = Input of int | Instr of ope * reg * operand

let ope_of_string ope =
    match ope with
    | "add" -> OpAdd | "mul" -> OpMul 
    | "div" -> OpDiv | "mod" -> OpMod 
    | "eql" -> OpEql
    | _ -> failwith "Invalid operation"

let reg_of_string r = match r with
    | "x" -> X | "y" -> Y | "z" -> Z | "w" -> W
    | _ -> failwith "Invalid register"

let operand_of_string op = match op with
    | "x" | "y" | "z" | "w" -> R (reg_of_string op)
    | _ -> C (int_of_string op)

let read_instr ic input =
    let tokens = String.split_on_char ' ' (input_line ic) in
    if List.hd tokens = "inp"
    then Input input
    else match tokens with
        | [ope; reg1; op] ->
                Instr (ope_of_string ope, reg_of_string reg1, operand_of_string op)
        | _ -> failwith "Invalid instruction"
    
let rec read_program ic input =
    try
        let i = read_instr ic input in
        let next_input = match i with Input _ -> input + 1 | _ -> input in
        i :: read_program ic next_input
    with End_of_file -> []

type expr = Add of expr * expr 
    | Mul of expr * expr
    | Div of expr * expr
    | Mod of expr * expr
    | Eql of expr * expr
    | Var of int
    | Constant of int

type abstract_alu = { x : expr; y : expr; z : expr; w : expr }

let string_of_ope ope = match ope with
    | OpAdd -> "add" | OpMul -> "mul" | OpDiv -> "div" | OpMod -> "mod" | OpEql -> "eql"
let string_of_reg r = match r with X -> "x" | Y -> "y" | Z -> "z" | W -> "w"
let string_of_op op = match op with R r -> string_of_reg r | C v -> string_of_int v
let string_of_instr i =
    match i with
    | Input i -> "inp w" ^ string_of_int i
    | Instr(ope, r, op) -> string_of_ope ope ^ " " ^ string_of_reg r ^ " " ^ string_of_op op

let rec div26 n = 
    if n = 0 then 0, 0
    else if n mod 26 <> 0 then n, 0
    else 
      let b, p = div26 (n / 26) in
        (b, p+1)

let rec string_of_expr ?(add_last=false) e =
    match e with
    | Add(e1, Constant v) when v < 0 -> "("^string_of_expr e1^string_of_int v^")"
    | Add(e1,e2) when add_last -> string_of_expr ~add_last:true e1^"+"^string_of_expr ~add_last:true e2
    | Add(e1,e2) -> "("^string_of_expr ~add_last:true e1^"+"^string_of_expr ~add_last:true e2^")"
    | Mul(e1,e2) -> string_of_expr e1^"*"^string_of_expr e2
    | Div(e1,e2) -> string_of_expr e1^"/"^string_of_expr e2
    | Mod(e1,e2) -> string_of_expr e1^"%"^string_of_expr e2
    | Eql(e1,e2) -> string_of_expr e1^"=="^string_of_expr e2
    | Var i -> "w"^string_of_int i
    | Constant i -> let b, p = div26 i in  
        let sb =  if b = 0 then "0" else if b = 1 then "" else string_of_int b in
        let sp = if p = 0 then "" else if p = 1 then "26" else "26^" ^ string_of_int p in
        if sb <> "" && sp <> ""
        then sb ^ "*" ^ sp
        else if sb = "" && sp = ""
        then "0"
        else sb ^ sp


let string_of_alu alu =
      "x = " ^ string_of_expr alu.x ^ "; "
    ^ "y = " ^ string_of_expr alu.y ^ "; "
    ^ "z = " ^ string_of_expr alu.z ^ "; "
    ^ "w = " ^ string_of_expr alu.w

let rec depth e =
    match e with
    | Add(e1,e2)
    | Mul(e1,e2)
    | Mod(e1,e2)
    | Div(e1,e2)
    | Eql(e1,e2) -> 1 + max (depth e1) (depth e2)
    | _ -> 0

let swap e1 e2 =
    if depth e1 < depth e2
    then true
    else match e1, e2 with
        | Constant 0, Constant v when v <> 0 -> true
        | Constant 1, Constant v when v <> 1 -> true
        | Constant _, Var _ -> true
        | Var _, Constant _ -> false
        | Var _, Var _ -> false
        | Var _, _ -> true
        | _ -> false

let rec bounds e = match e with
    | Constant v -> (v, v)
    | Var _ -> (1, 9)
    | Add(e1, e2) -> 
            let min1, max1 = bounds e1 in
            let min2, max2 = bounds e2 in
            (min1+min2, max1+max2)
    | Eql(_,_) -> (0, 1)
    | Div(e,Constant v) -> let mn, mx = bounds e in (mn/v, mx/v)
    | Mod(_,Constant v) -> (0, v-1)
    | _ -> (-100000,100000)


let rec simpl e =
    match e with
    | Add(e', Constant 0) -> simpl e'
    | Add(e1, Add(e2,e3)) -> simpl(Add(Add(e1,e2),e3))
    | Mul(e1, Mul(e2,e3)) -> simpl(Mul(Mul(e1,e2),e3))
    | Add(Add(e',Constant v1), Constant v2) -> simpl (Add(e',Constant(v1+v2)))

    | Add(Add(e1,Constant v), e2) -> simpl (Add(Add(e1,e2),Constant v))

    | Mul(Mul(e',Constant v1), Constant v2) -> simpl (Mul(e',Constant(v1*v2)))
    | Div(Div(e',Constant v1), Constant v2) -> simpl (Div(e',Constant(v1*v2)))
    | Add(Constant v1, Constant v2) -> Constant (v1+v2)
    | Mul(Constant v1, Constant v2) -> Constant (v1*v2)
    | Div(Constant v1, Constant v2) -> Constant (v1/v2)
    | Mod(Constant v1, Constant v2) -> Constant (v1 mod v2)
    | Mul(e', Constant 0) -> Constant 0
    | Mul(e', Constant 1) -> simpl e'
    | Div(Mul(e', Constant v), Constant w) when v = w -> simpl e'
    | Mod(Constant 0, _) -> Constant 0
    | Div(e', Constant 1) -> simpl e'
    | Div(e', Constant v) when snd (bounds e') < v -> Constant 0
    | Mod(Mul(e1,Constant w), Constant v) when w mod v = 0 -> Constant 0
    | Div(Mul(e1,Constant w), Constant v) when w mod v = 0 -> Mul(e1, Constant(w / v))
    | Mod(Add(e1,e2), e') -> simpl (Add(Mod(e1, e'), Mod(e2, e')))
    | Mul(Add(e1,e2), e') -> simpl (Add(Mul(e1, e'), Mul(e2, e')))
    | Div(Add(e1,e2), e') -> simpl (Add(Div(e1, e'), Div(e2, e')))
    | Mod(e', Constant v) ->
            let e' = simpl e' in
            let mn, mx = bounds e' in
            if mx < v then e' else Mod(e', Constant v)

    | Eql(Var _, Constant n) when n < 1 || n > 9 -> Constant 0
    | Eql(e', Var _) when fst(bounds e') > 9 -> Constant 0
    | Eql(Constant m, Constant n) -> Constant (if m = n then 1 else 0)

    | Add(e1,e2) when swap e1 e2 -> simpl(Add(e2,e1))
    | Mul(e1,e2) when swap e1 e2 -> simpl(Mul(e2,e1))
    | Eql(e1,e2) when swap e1 e2 -> simpl(Eql(e2,e1))

    | Add(e1, e2) -> let e'1 = simpl e1 in let e'2 = simpl e2 in
        if e'1 <> e1 || e'2 <> e2 then simpl(Add(e'1,e'2)) else e
    | Mul(e1, e2) -> let e'1 = simpl e1 in let e'2 = simpl e2 in
        if e'1 <> e1 || e'2 <> e2 then simpl(Mul(e'1,e'2)) else e
    | Mod(e1, e2) -> let e'1 = simpl e1 in let e'2 = simpl e2 in
        if e'1 <> e1 || e'2 <> e2 then simpl(Mod(e'1,e'2)) else e
    | Div(e1, e2) -> let e'1 = simpl e1 in let e'2 = simpl e2 in
        if e'1 <> e1 || e'2 <> e2 then simpl(Div(e'1,e'2)) else e
    | Eql(e1, e2) -> let e'1 = simpl e1 in let e'2 = simpl e2 in
        if e'1 <> e1 || e'2 <> e2 then simpl(Eql(e'1,e'2)) else e
    | _ -> e

let apply instr alu =
    let { x = x; y = y; z = z; w = w } = alu in
    let set_reg r v =
        Printf.printf "simpl %s -> " (string_of_expr v);
        let v = simpl v in
        Printf.printf "%s\n" (string_of_expr v);
        match r with
        | X -> { alu with x = v }
        | Y -> { alu with y = v }
        | Z -> { alu with z = v }
        | W -> { alu with w = v }
    in
    let get_reg r = match r with X -> x | Y -> y | Z -> z | W -> w in
    let get_ope ope = match ope with
        | R r -> get_reg r 
        | C v -> Constant v
    in
    match instr with
    | Input i -> { alu with w = Var i }, None
    | Instr(OpAdd, r1, ope) -> set_reg r1 (Add(get_reg r1, get_ope ope)), None
    | Instr(OpMul, r1, ope) -> set_reg r1 (Mul(get_reg r1, get_ope ope)), None
    | Instr(OpDiv, r1, ope) -> set_reg r1 (Div(get_reg r1, get_ope ope)), None
    | Instr(OpMod, r1, ope) -> set_reg r1 (Mod(get_reg r1, get_ope ope)), None
    | Instr(OpEql, r1, ope) -> 
            begin
                (* Branching prediction *)
                let e' = simpl (Eql(get_reg r1, get_ope ope)) in
                match e' with
                | Eql(e1, e2) -> set_reg r1 (Constant 1), Some (e1, e2) (* always branch equal *)
                | _ -> set_reg r1 e', None
            end

let rec get_var e = 
    match e with
    | Add(e1,e2) | Mul(e1,e2) | Mod(e1,e2) | Div(e1,e2) | Eql(e1,e2)  -> get_var e1 @ get_var e2
    | Var i -> [ i ]
    | _ -> []

let rec reduce e v =
    match e with
    | Add(e1,e2) -> (reduce e1 v) + (reduce e2 v)
    | Mul(e1,e2) -> (reduce e1 v) * (reduce e2 v)
    | Div(e1,e2) -> (reduce e1 v) / (reduce e2 v)
    | Mod(e1,e2) -> (reduce e1 v) mod (reduce e2 v)
    | Eql(e1,e2) -> if reduce e1 v = reduce e2 v then 1 else 0
    | Constant c -> c
    | Var _ -> v
    
let rec digit d p =
    if p = 0 then d else 10 * digit d (p-1)

let unify pair =
    match pair with
    | e, Var i -> begin
        match get_var e with
        | [ j ] ->
            List.fold_left (@) []
                (List.init 9 (fun v -> let r = reduce e (v+1) in
                    if 0 < r && r < 10
                    then [digit (v+1) (14-j) + digit r (14-i)]
                    else []))
        | _ -> failwith "Invalid pair"
        end
    | _ -> failwith "Invalid pair"


let rec expand l =
    match l with
    | sl::l' ->
        let el' = expand l' in
        List.fold_left (@) []
            (List.map
                (fun n -> List.map ((+) n) el') sl)
    | [] -> [ 0 ]
            
let main =
    let ic = open_in "input.txt" in
    let program = read_program ic 1 in
    let alu = {x=Constant 0; y=Constant 0; z = Constant 0; w=Constant 0 } in
    let rec eval p alu =
        match p with
        | i::p' -> 
           let alu', unification = apply i alu in
            Printf.printf "%s\n" (string_of_instr i);
            Printf.printf "%s\n" (string_of_alu alu');
            let unifications = eval p' alu' in
            begin
                match unification with
                | None -> unifications
                | Some pair -> pair :: unifications
            end
        | [] -> []
    in
    let unifications = eval program alu in
    List.iter
        (fun (e1,e2) -> Printf.printf "%s == %s\n" 
            (string_of_expr e1) (string_of_expr e2))
        unifications;
    let cases = List.map unify unifications in
    let numbers = expand cases in
    let l = List.sort compare numbers in
    let part1 = List.hd l in
    let part2 = List.hd (List.rev l) in
    Printf.printf "Part 1: %d\nPart 2: %d\n" part1 part2;
    unifications, cases
