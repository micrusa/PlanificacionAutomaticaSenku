(define (domain senku-domain)
 (:requirements :strips :typing :negative-preconditions)
 (:types casilla)
 (:predicates 
             (ocupada ?casilla - casilla)
             (movimiento_valido ?de - casilla ?sobre - casilla ?a - casilla)
 )
 (:action saltar
  :parameters ( ?de - casilla ?sobre - casilla ?a - casilla)
  :precondition (and (movimiento_valido ?de ?sobre ?a) (ocupada ?de) (ocupada ?sobre) (not (ocupada ?a)))
  :effect (and (not (ocupada ?de)) (not (ocupada ?sobre)) (ocupada ?a)))
)
