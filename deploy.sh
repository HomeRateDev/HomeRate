if [ $TRAVIS_BRANCH == 'master' ]
then
  echo "Deploy running."
  ssh -o "StrictHostKeyChecking no" django@homerate.co.uk "cd HomeRate && ./reload.sh && exit"
  echo "Deploy complete."
fi
