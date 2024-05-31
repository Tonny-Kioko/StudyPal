#!/usr/bin/env bash
# Use this script to test if a given TCP host/port are available

TIMEOUT=15
QUIET=0
WAITFORIT_host=
WAITFORIT_port=

echoerr() {
  if [[ $QUIET -ne 1 ]]; then echo "$@" 1>&2; fi
}

usage() {
  exitcode="$1"
  cat << USAGE >&2
Usage:
  $0 host:port [-t timeout] [-q] [-- command args]
  -h HOST | --host=HOST       Host or IP under test
  -p PORT | --port=PORT       TCP port under test
                              Alternatively, you specify the host and port as host:port
  -t TIMEOUT | --timeout=TIMEOUT
                              Timeout in seconds, zero for no timeout
  -q | --quiet                Don't output any status messages
  -- COMMAND ARGS             Execute command with args after the test finishes
USAGE
  exit "$exitcode"
}

wait_for() {
  if [[ $TIMEOUT -gt 0 ]]; then
    echoerr "$0: waiting $TIMEOUT seconds for $WAITFORIT_host:$WAITFORIT_port"
  else
    echoerr "$0: waiting for $WAITFORIT_host:$WAITFORIT_port without a timeout"
  fi
  start_ts=$(date +%s)
  while :
  do
    if [[ $WAITFORIT_is_host_port_avail -eq 1 ]]; then
      (echo > /dev/tcp/$WAITFORIT_host/$WAITFORIT_port) >/dev/null 2>&1
    else
      nc -z "$WAITFORIT_host" "$WAITFORIT_port" >/dev/null 2>&1
    fi
    result=$?
    if [[ $result -eq 0 ]]; then
      end_ts=$(date +%s)
      echoerr "$0: $WAITFORIT_host:$WAITFORIT_port is available after $((end_ts - start_ts)) seconds"
      break
    fi
    sleep 1
  done
  return $result
}

wait_for_wrapper() {
  if [[ $QUIET -eq 1 ]]; then
    "$@" &>/dev/null &
  else
    "$@" &
  fi
  wait $!
  return $?
}

parse_args() {
  while [[ $# -gt 0 ]]
  do
    case "$1" in
      *:* )
      WAITFORIT_host=$(echo "$1" | cut -d : -f 1)
      WAITFORIT_port=$(echo "$1" | cut -d : -f 2)
      shift 1
      ;;
      -h)
      WAITFORIT_host="$2"
      if [[ $WAITFORIT_host == "" ]]; then break; fi
      shift 2
      ;;
      --host=*)
      WAITFORIT_host="${1#*=}"
      shift 1
      ;;
      -p)
      WAITFORIT_port="$2"
      if [[ $WAITFORIT_port == "" ]]; then break; fi
      shift 2
      ;;
      --port=*)
      WAITFORIT_port="${1#*=}"
      shift 1
      ;;
      -t)
      TIMEOUT="$2"
      if [[ $TIMEOUT == "" ]]; then break; fi
      shift 2
      ;;
      --timeout=*)
      TIMEOUT="${1#*=}"
      shift 1
      ;;
      -q | --quiet)
      QUIET=1
      shift 1
      ;;
      --)
      shift
      break
      ;;
      --help)
      usage 0
      ;;
      *)
      echoerr "Unknown argument: $1"
      usage 1
      ;;
    esac
  done

  if [[ "$WAITFORIT_host" == "" || "$WAITFORIT_port" == "" ]]; then
    echoerr "Error: you need to provide a host and port to test."
    usage 2
  fi
}

main() {
  parse_args "$@"
  wait_for
  result=$?
  if [[ $result -ne 0 ]]; then
    echoerr "$0: timeout occurred after waiting $TIMEOUT seconds for $WAITFORIT_host:$WAITFORIT_port"
  fi
  if [[ "$#" -gt 0 ]]; then
    wait_for_wrapper "$@"
  fi
  exit $result
}

WAITFORIT_is_host_port_avail=1
main "$@"
