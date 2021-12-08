
let ic = open_in "example.txt"

let read_one_line () = 
    let s = input_line ic in
    let i = String.index s '|' in
    let patterns = String.split_on_char ' ' (String.sub s 0 (i-1)) in
    let targets =  String.split_on_char ' ' (String.sub s (i+2) 
                           (String.length s - i - 2)) in
    patterns, targets

let rec read_all () =
    try
        let c = read_one_line () in
        c :: read_all ()
    with End_of_file -> []

let data = read_all ()
