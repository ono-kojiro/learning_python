(
  echo "First shell"
) & (
  sleep 1
  echo "Second shell"
) &

wait

