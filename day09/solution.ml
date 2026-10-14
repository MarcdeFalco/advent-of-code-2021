(* Advent of Code 2021, jour 9.
   Partie 1 : un point bas est une case strictement plus basse que ses
   quatre voisins.
   Partie 2 : chaque bassin est la composante connexe d'un point bas dans
   le graphe des cases de hauteur différente de 9, mesurée par un parcours
   en profondeur récursif. *)

let digit c =
  match c with
  | '0' .. '9' -> int_of_char c - int_of_char '0'
  | _ -> failwith "caractère invalide"

let lire_grille nom =
  let ic = open_in nom in
  let rec lire () =
    match input_line ic with
    | s -> (String.to_seq s |> Array.of_seq |> Array.map digit) :: lire ()
    | exception End_of_file -> close_in ic; []
  in
  Array.of_list (lire ())

let hmap = lire_grille "input.txt"
let w = Array.length hmap.(0)
let h = Array.length hmap

let valid_coord (x, y) = 0 <= x && x < w && 0 <= y && y < h

let voisins (x, y) =
  List.filter valid_coord [ (x - 1, y); (x + 1, y); (x, y - 1); (x, y + 1) ]

let low_point (x, y) =
  let min_voisins =
    List.fold_left min 9 (List.map (fun (x, y) -> hmap.(y).(x)) (voisins (x, y)))
  in
  min_voisins > hmap.(y).(x)

let all_coords =
  List.concat (List.init w (fun x -> List.init h (fun y -> (x, y))))

let low_points = List.filter low_point all_coords

(* Taille du bassin contenant (x, y) : nombre de cases atteintes par le
   parcours, sans traverser les cases de hauteur 9. *)
let basin (x, y) =
  let visited = Array.make_matrix h w false in
  let rec visit (x, y) =
    if visited.(y).(x) then 0
    else begin
      visited.(y).(x) <- true;
      List.fold_left ( + ) 1
        (List.map
           (fun (vx, vy) ->
              if not visited.(vy).(vx) && hmap.(vy).(vx) <> 9 then visit (vx, vy)
              else 0)
           (voisins (x, y)))
    end
  in
  visit (x, y)

let partie1 () =
  List.fold_left ( + ) 0 (List.map (fun (x, y) -> 1 + hmap.(y).(x)) low_points)

let partie2 () =
  let basins = List.map basin low_points in
  match List.rev (List.sort compare basins) with
  | a :: b :: c :: _ -> a * b * c
  | _ -> failwith "moins de trois bassins"

let () =
  Printf.printf "Partie 1 : %d\n" (partie1 ());
  Printf.printf "Partie 2 : %d\n" (partie2 ())
