from jose import jwt


def validate_token(token):
    return jwt.decode(
        token,
        key="password",
        audience="https://pyconus2024.com",
        algorithms="HS256"
    )


token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJodHRwczovL2F1dGguYXBpdGhyZWF0cy5jb20iLCJzdWIiOiIxMCIsImF1ZCI6Imh0dHBzOi8vcHljb251czIwMjQuY29tIiwiaWF0IjoxNzE1ODAyMDc2LjMwMDc0NCwiZXhwIjoxNzE1ODA1Njc2LjMwMDc0NH0.XYwI7fQNb09nHKMPMv2-Bl1O9EzpwFo_dcp0WpEiCsg"
print(validate_token(token))
