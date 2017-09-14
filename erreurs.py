class ErreurConsistance(Exception):
    """Erreur levée lorsqu'une inconsistance est détectée dans les entrées."""
    def __str__(self):
        return "Erreur de consistance"
