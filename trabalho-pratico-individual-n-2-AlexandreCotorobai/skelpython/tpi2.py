#encoding: utf8

# YOUR NAME: Alexandre Cotorobai
# YOUR NUMBER: 107849

# COLLEAGUES WITH WHOM YOU DISCUSSED THIS ASSIGNMENT (names, numbers):
# - ...
# - ...

from semantic_network import *
from constraintsearch import *

class MySN(SemanticNetwork):

    def __init__(self):
        SemanticNetwork.__init__(self)
        # ADD CODE HERE IF NEEDED
        self.assoc_stats = {}

    def query_local(self,user=None,e1=None,rel=None,e2=None):
        # IMPLEMENT HERE
        self.query_result = []

        for user_key, declarations_for_user in self.declarations.items():
            for key, value in declarations_for_user.items():
                entity1, relation_name = key
                entity2 = value

                if (user is None or user == user_key) \
                        and (e1 is None or entity1 == e1) \
                        and (rel is None or relation_name == rel) \
                        and (e2 is None or entity2 == e2):
                    if isinstance(entity2, set):
                        self.query_result.extend([
                            Declaration(user_key, Relation(entity1, relation_name, item))
                            for item in entity2
                        ])
                    else:
                        self.query_result.append(Declaration(user_key, Relation(entity1, relation_name, entity2)))
                    # self.query_result.append(Declaration(user_key, Relation(entity1, relation_name, entity2)))

        return self.query_result # Your code must leave the output in
                          # self.query_result, which is returned here

    def query(self,entity,assoc=None):
        # # IMPLEMENT HERE
        # pass
        # return self.query_result # Your code must leave the output in
        #                   # self.query_result, which is returned here
        decl = self.query_local(e1=entity, rel=assoc)

        pred = [d.relation.entity2 for d in self.query_local(e1=entity)]

        for p in pred:
            decl += self.query(entity=p, assoc=assoc)
        
        decl = [d for d in decl if 'member' not in str(d) and 'subtype' not in str(d)]

        
        return decl


    def update_assoc_stats(self,assoc,user=None):
        # IMPLEMENT HERE
        stats_assoc_e1 = {}
        stats_assoc_e2 = {}

        local_declarations = self.query_local(user=user, rel=assoc)

        unknown1 = unknown2 = objects1 = objects2 = 0

        for declaration in local_declarations:
            e1 = declaration.relation.entity1 if isObjectName(declaration.relation.entity1) else None
            e2 = declaration.relation.entity2 if isObjectName(declaration.relation.entity2) else None

            stats_assoc_e1, unknown1, objects1 = self.update_stats(e1, stats_assoc_e1, unknown1, objects1, user)
            stats_assoc_e2, unknown2, objects2 = self.update_stats(e2, stats_assoc_e2, unknown2, objects2, user)

        total_objects_1 = objects1 - unknown1 + unknown1 ** 0.5
        total_objects_2 = objects2 - unknown2 + unknown2 ** 0.5

        for tipo in stats_assoc_e1:
            stats_assoc_e1[tipo] /= total_objects_1

        for tipo in stats_assoc_e2:
            stats_assoc_e2[tipo] /= total_objects_2

        self.assoc_stats[(assoc, user)] = (stats_assoc_e1, stats_assoc_e2)

    def update_stats(self, item, freq_dict, unknown_count, total_count, user):
        if item:
            item_types = self.get_types(item, user)
            unknown_count += len(item_types) == 0
            for tipo in item_types:
                if tipo not in freq_dict:
                    freq_dict[tipo] = 1
                else:
                    freq_dict[tipo] += 1
            total_count += 1
        return freq_dict, unknown_count, total_count

    def get_types(self, obj, user=None):
        types = set()

        rel = [d for d in self.query_local(user=user, e1=obj) if "subtype" in str(d.relation) or "member" in str(d.relation)] 

        for d in rel:
            if d.relation.entity1 == obj and isTypeName(d.relation.entity2):
                types.update([d.relation.entity2] + list(self.get_types(d.relation.entity2, user=user)))
            elif d.relation.entity2 == obj and isObjectName(d.relation.entity1):
                types.update([d.relation.entity1] + list(self.get_types(d.relation.entity1, user=user)))

        return types

class MyCS(ConstraintSearch):

    def __init__(self,domains,constraints):
        ConstraintSearch.__init__(self,domains,constraints)
        self.solutions = []
        self.variables = list(domains.keys())

    def search_all(self, domains=None, xpto=None):
        if domains is None:
            domains = self.domains
        if xpto is None:
            xpto = {}

        self._search_all(domains, xpto)
        return self.solutions

    def _search_all(self, domains, assignment):

        if any(len(lv) == 0 for lv in domains.values()):
            return None
        
        if len(assignment) == len(self.variables):
            if assignment not in self.solutions:
                self.solutions.append(assignment.copy())
            return

        var = self.variable_ordering(domains, assignment)

        for value in domains[var]:
            if self.consistent(var, value, assignment):
                assignment[var] = value
                new_domains = self.propagate(domains, var, value)
                if new_domains is not None:
                    self._search_all(new_domains, assignment)
                assignment.pop(var, None)

    def variable_ordering(self, domains, assignment):
        x = sorted(domains.keys(), key=lambda var: len(domains[var]))
        return next(v for v in x if v not in assignment)
        
    def propagate(self, domains, var, value):
        new_domain = domains.copy()
        for v, domain in domains.items():
            
            if v != var and (v, var) in self.constraints:
                constraint = self.constraints[v, var]
                new_domain[v] = [val for val in new_domain[v] if constraint(v, val, var, value)]
                if not new_domain[v]:
                    return None

        return new_domain

    
    def consistent(self, var, value, assignment):
        assignment_copy = assignment.copy()
        assignment_copy.pop(var, None)

        for other_var, other_value in assignment_copy.items():
            constraint = self.constraints.get((var, other_var))
            if constraint and not constraint(var, value, other_var, other_value):
                return False

        return True