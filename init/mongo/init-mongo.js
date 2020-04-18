db.createUser({
    user: 'developer',
    pwd: 'developer',
    roles: [
        {
            role: 'readWrite',
            db: 'masterthesis'
        }
    ]

})

// https://medium.com/faun/managing-mongodb-on-docker-with-docker-compose-26bf8a0bbae3