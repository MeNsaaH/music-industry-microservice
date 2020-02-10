FROM golang:1.13-alpine as builder

ENV PROJECT github.com/mensaah/music-industry-microservice/video

WORKDIR /go/src/$PROJECT

COPY . .
RUN go build -gcflags='-N -l' -o /video .

COPY --from=builder /video /video

EXPOSE 5050
ENTRYPOINT ["/video"]
